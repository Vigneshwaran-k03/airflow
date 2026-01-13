from sqlalchemy import select, table, column, func, cast, String
from sqlalchemy.orm import aliased
from models.translation import Translate




# Tables
arborescence = table(
    "arborescence",
    column("id"),
    column("id_parent"),
    column("tr_nom"),
    column("tr_label"),
    column("tr_sommaire"),
    column("tr_alias"),
    column("img"),
    column("default_machine_img"),
    column("background"),
    column("icon"),
    column("code_douane"),
    column("poids_moyen"),
    column("has_battery"),
    column("depreciation_rate"),
    column("is_visible_front"),
)

parent_ids_tbl = table(
    "arborescence_parent_ids",
    column("id"),
    column("parent_ids"),
)
def universal_environment_query():
    f_produits_machine = table(
        "f_produits_machine",
        column("id_arborescence"),
        column("id_produit"),
    )

    environment_product = table(
        "#environment_product",
        column("product_id"),
        column("environment_id"),
    )

    environment = table(
        "environment",
        column("id"),
        column("label"),
    )

    # ---- INNER DISTINCT SUBQUERY ----
    distinct_env = (
        select(
            f_produits_machine.c.id_arborescence.label("id"),
            environment.c.label.label("label"),
        )
        .select_from(
            f_produits_machine
            .outerjoin(
                environment_product,
                environment_product.c.product_id == f_produits_machine.c.id_produit,
            )
            .outerjoin(
                environment,
                environment.c.id == environment_product.c.environment_id,
            )
        )
        .distinct()
        .subquery("distinct_env")
    )

    # ---- JSON AGGREGATION ----
    return (
        select(
            distinct_env.c.id,
            func.coalesce(
                func.json_arrayagg(distinct_env.c.label),
                func.json_array(),
            ).label("environment"),
        )
        .group_by(distinct_env.c.id)
    )


def universal_base_query(limit=None, offset=None):
    TrName = aliased(Translate)
    TrLabel = aliased(Translate)
    TrSummary = aliased(Translate)
    TrAlias = aliased(Translate)

    env_subq = universal_environment_query().subquery("env")

    return (
        select(
            arborescence.c.id,
            arborescence.c.id_parent.label("parent_id"),
            parent_ids_tbl.c.parent_ids,

            cast(func.json_object(*Translate.json_args(TrName)), String).label("name"),
            cast(func.json_object(*Translate.json_args(TrLabel)), String).label("label"),
            cast(func.json_object(*Translate.json_args(TrSummary)), String).label("summary"),
            cast(func.json_object(*Translate.json_args(TrAlias)), String).label("alias"),

            arborescence.c.img,
            arborescence.c.default_machine_img,
            arborescence.c.background,
            arborescence.c.icon,
            arborescence.c.code_douane.label("customs_code"),
            arborescence.c.poids_moyen.label("average_weight"),
            arborescence.c.has_battery,
            arborescence.c.depreciation_rate,
            arborescence.c.is_visible_front,

            env_subq.c.environment,
        )
        .outerjoin(TrName, TrName.id == arborescence.c.tr_nom)
        .outerjoin(TrLabel, TrLabel.id == arborescence.c.tr_label)
        .outerjoin(TrSummary, TrSummary.id == arborescence.c.tr_sommaire)
        .outerjoin(TrAlias, TrAlias.id == arborescence.c.tr_alias)
        .outerjoin(parent_ids_tbl, parent_ids_tbl.c.id == arborescence.c.id)
        .outerjoin(env_subq, env_subq.c.id == arborescence.c.id)
        .limit(limit)
        .offset(offset)
    )
