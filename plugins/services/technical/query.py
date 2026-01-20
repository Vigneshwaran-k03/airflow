from sqlalchemy import select, table, column, cast, func, String
from sqlalchemy.orm import aliased
from models.translation import Translate
from models.technicals import Technical, TechnicalParentIds
from sqlalchemy.sql import distinct

def technical_base_query(limit=None, offset=None):
    TrName = aliased(Translate)
    TrLabel = aliased(Translate)
    env_subq = technical_environment_query().subquery("tech_env")

    return (
        select(
            #ids
            Technical.id.label("id"),
            Technical.id_parent.label("parent_id"),
            TechnicalParentIds.parent_ids.label("parent_ids"),

            #environment
            env_subq.c.environments.label("environments"),

            Technical.poids.label("weight"),
            Technical.is_consommable.label("is_consumable"),
            Technical.is_accessory,
            Technical.is_other,
            Technical.conditionnement.label("packaging"),
            Technical.is_visible,
            Technical.hs_code,
            Technical.score,
            Technical.img.label("picture"),

            # translations (JSON as STRING – flattened later)
            cast(func.json_object(*Translate.json_args(table=TrName)), String).label("name"),
            cast(func.json_object(*Translate.json_args(table=TrLabel)), String).label("label"),
        )
        .select_from(Technical)
        .outerjoin(TrName, TrName.id == Technical.nom)
        .outerjoin(TrLabel, TrLabel.id == Technical.label)
        .outerjoin(TechnicalParentIds, TechnicalParentIds.id == Technical.id)
        .outerjoin(env_subq, env_subq.c.id == Technical.id)
        .limit(limit)
        .offset(offset)
    )

def technical_environment_query(ids: list[int] = None):
    f_produits_piece = table(
        "f_produits_piece",
        column("id"),
        column("id_branche_technique"),
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

    return (
        select(
            f_produits_piece.c.id.label("id"),

            # Always return an array (empty if nothing found)
            func.coalesce(
                func.json_arrayagg(
                    environment.c.label
                ),
                func.json_array()
            ).label("environments"),
        )
        .select_from(
            f_produits_piece
            .outerjoin(
                environment_product,
                environment_product.c.product_id
                == f_produits_piece.c.id_branche_technique
            )
            .outerjoin(
                environment,
                environment.c.id
                == environment_product.c.environment_id
            )
        )
        .where(
            f_produits_piece.c.id.in_(ids) if ids is not None else True
        )
        .group_by(f_produits_piece.c.id)
    )
