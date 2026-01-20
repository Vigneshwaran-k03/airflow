from sqlalchemy import select, table, column, func, cast, String
from sqlalchemy.orm import aliased
from models.translation import Translate
from models.universals import Universal, UniversalParentIds


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
            Universal.id,
            Universal.id_parent.label("parent_id"),
            UniversalParentIds.parent_ids,

            cast(func.json_object(*Translate.json_args(table=TrName)), String).label("name"),
            cast(func.json_object(*Translate.json_args(table=TrLabel)), String).label("label"),
            cast(func.json_object(*Translate.json_args(table=TrSummary)), String).label("summary"),
            cast(func.json_object(*Translate.json_args(table=TrAlias)), String).label("alias"),

            Universal.img,
            Universal.default_machine_img,
            Universal.background,
            Universal.icon,
            Universal.code_douane.label("customs_code"),
            Universal.poids_moyen.label("average_weight"),
            Universal.has_battery,
            Universal.depreciation_rate,
            Universal.is_visible_front,

            env_subq.c.environment,
        )
        .select_from(Universal)
        .outerjoin(TrName, TrName.id == Universal.tr_nom)
        .outerjoin(TrLabel, TrLabel.id == Universal.tr_label)
        .outerjoin(TrSummary, TrSummary.id == Universal.tr_sommaire)
        .outerjoin(TrAlias, TrAlias.id == Universal.tr_alias)
        .outerjoin(UniversalParentIds, UniversalParentIds.id == Universal.id)
        .outerjoin(env_subq, env_subq.c.id == Universal.id)
        .limit(limit)
        .offset(offset)
    )
