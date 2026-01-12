from sqlalchemy import select, table, column, cast, func, String 
from sqlalchemy.orm import aliased
from models.translation import Translate
from sqlalchemy.sql import distinct

arbre_kit_technique = table(
    "arbre_kit_technique",
    column("id"),
    column("id_parent"),
    column("nom"),
    column("label"),
    column("poids"),
    column("is_consommable"),
    column("is_accessory"),
    column("is_other"),
    column("conditionnement"),
    column("is_visible"),
    column("img"),
    column("hs_code"),
    column("score"),
)
tech_parent_ids = table(
    "tech_parent_ids",
    column("id"),
    column("parent_ids"),
)

def technical_base_query(limit=None, offset=None):
    TrName = aliased(Translate)
    TrLabel = aliased(Translate)
    env_subq = technical_environment_query().subquery("tech_env")

    return (
        select(
            #ids
            arbre_kit_technique.c.id.label("id"),
            arbre_kit_technique.c.id_parent.label("parent_id"),
            tech_parent_ids.c.parent_ids.label("parent_ids"),

            #environment
            env_subq.c.environments.label("environments"),

            arbre_kit_technique.c.poids.label("weight"),
            arbre_kit_technique.c.is_consommable.label("is_consumable"),
            arbre_kit_technique.c.is_accessory,
            arbre_kit_technique.c.is_other,
            arbre_kit_technique.c.conditionnement.label("packaging"),
            arbre_kit_technique.c.is_visible,
            arbre_kit_technique.c.hs_code,
            arbre_kit_technique.c.score,
            arbre_kit_technique.c.img.label("picture"),

            # translations (JSON as STRING – flattened later)
            cast(func.json_object(*Translate.json_args(table=TrName)), String).label("name"),
            cast(func.json_object(*Translate.json_args(table=TrLabel)), String).label("label"),
        )
        .outerjoin(TrName, TrName.id == arbre_kit_technique.c.nom)
        .outerjoin(TrLabel, TrLabel.id == arbre_kit_technique.c.label)
        .outerjoin(tech_parent_ids,tech_parent_ids.c.id == arbre_kit_technique.c.id)
        .outerjoin(env_subq, env_subq.c.id == arbre_kit_technique.c.id)
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
