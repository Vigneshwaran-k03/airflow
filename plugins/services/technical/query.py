from sqlalchemy import select, table, column, cast, func, String
from sqlalchemy.orm import aliased
from models.translation import Translate

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

    return (
        select(
            arbre_kit_technique.c.id.label("id"),
            arbre_kit_technique.c.id_parent.label("parent_id"),
            tech_parent_ids.c.parent_ids.label("parent_ids"),

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
        .limit(limit)
        .offset(offset)
    )
