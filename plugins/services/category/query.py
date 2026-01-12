from sqlalchemy import (
    select,
    func,
    cast,
    String,
    table,
    column,
)
from sqlalchemy.orm import aliased

from models.translation import Translate

#DEFINE TABLE
catman_swap = table(
    "catman_swap",
    column("id"),
    column("id_parent"),
    column("tr_nom"),
    column("tr_label"),
    column("tr_title"),
    column("tr_desc"),
    column("tr_desc_long"),
    column("tr_metadesc"),
    column("tr_metatitle"),
    column("ordre"),
    column("is_visible"),
    column("is_enable"),
    column("is_clickable"),
    column("aff_piece"),
    column("is_reconditioned"),
    column("is_excluded_from_naming"),
    column("has_generated_children"),
    column("is_visible_menu"),
    column("alias"),
    column("score"),
    column("event"),
    column("img_picto"),
    column("img"),
    column("environment"),
    column("id_environment"),
    column("link_type"),
    column("generated_title"),
)
catman_parent_ids = table(
    "catman_parent_ids",
    column("child_id"),
    column("parent_ids"),
)

# Define l_catman_swap table for branches
l_catman_swap = table(
    "l_catman_swap",
    column("id_catman"),
    column("id_cible"),
    column("table_cible"),
)

def categories_base_query(limit: int = None, offset: int = None):
    # Create subqueries for technical and universal branches
    technical_branches_sq = (
        select(
            l_catman_swap.c.id_catman.label("catman_id"),
            func.json_arrayagg(l_catman_swap.c.id_cible).label("technical_branches"),
        )
        .where(l_catman_swap.c.table_cible == "arbre_kit_technique")
        .group_by(l_catman_swap.c.id_catman)
        .subquery()
    )
    
    universal_branches_sq = (
        select(
            l_catman_swap.c.id_catman.label("catman_id"),
            func.json_arrayagg(l_catman_swap.c.id_cible).label("universal_branches"),
        )
        .where(l_catman_swap.c.table_cible == "arborescence")
        .group_by(l_catman_swap.c.id_catman)
        .subquery()
    )

    Parent = aliased(catman_swap)
    RootParent = aliased(catman_swap)
    TrGeneratedTitle = aliased(Translate)
    TrName = aliased(Translate)
    TrLabel = aliased(Translate)
    TrTitle = aliased(Translate)
    TrDesc = aliased(Translate)
    TrDescLong = aliased(Translate)
    TrMetaDesc = aliased(Translate)
    TrMetaTitle = aliased(Translate)

    return (
        select(
            # IDs
            catman_swap.c.id.label("id"),
            catman_swap.c.id_parent.label("parent_id"),
            catman_parent_ids.c.parent_ids.label("parent_ids"),

            # Order
            catman_swap.c.ordre.label("order"),

            # Flags
            catman_swap.c.is_visible,
            catman_swap.c.is_enable.label("is_enabled"),
            catman_swap.c.is_clickable,
            catman_swap.c.aff_piece.label("has_pieces_displayed"),
            catman_swap.c.is_reconditioned,
            catman_swap.c.is_excluded_from_naming,
            catman_swap.c.is_visible_menu,
            catman_swap.c.has_generated_children,

            #environment
            catman_swap.c.environment,
            catman_swap.c.id_environment,
            
            #linktype
            catman_swap.c.link_type,

            # Other fields
            catman_swap.c.alias,
            catman_swap.c.score,
            catman_swap.c.event,

            #images
            catman_swap.c.img_picto.label("icon"),
            catman_swap.c.img.label("picture"),

            #parents
            Parent.c.img.label("parent_picture"),
            cast(func.json_object(*Translate.json_args(table=TrName)), String).label("parent_name"),
            cast(func.json_object(*Translate.json_args(table=TrLabel)), String).label("parent_label"),

            # Branches
            technical_branches_sq.c.technical_branches,
            universal_branches_sq.c.universal_branches,

            # Translations (JSON as STRING – flattened later)
            cast(func.json_object(*Translate.json_args(table=TrName)), String).label("name"),
            cast(func.json_object(*Translate.json_args(table=TrLabel)), String).label("label"),
            cast(func.json_object(*Translate.json_args(table=TrTitle)), String).label("title"),
            cast(func.json_object(*Translate.json_args(table=TrDesc)), String).label("description"),
            cast(func.json_object(*Translate.json_args(table=TrDescLong)), String).label("long_description"),
            cast(func.json_object(*Translate.json_args(table=TrMetaTitle)), String).label("meta_title"),
            cast(func.json_object(*Translate.json_args(table=TrMetaDesc)), String).label("meta_description"),
            cast(func.json_object(*Translate.json_args(table=TrGeneratedTitle)),String).label("generated_title"),

    

        )
        .select_from(catman_swap)
        .outerjoin(Parent, Parent.c.id == catman_swap.c.id_parent)
        .outerjoin(RootParent, RootParent.c.id == Parent.c.id_parent)
        .outerjoin(TrName, TrName.id == catman_swap.c.tr_nom)
        .outerjoin(TrLabel, TrLabel.id == catman_swap.c.tr_label)
        .outerjoin(TrTitle, TrTitle.id == catman_swap.c.tr_title)
        .outerjoin(TrDesc, TrDesc.id == catman_swap.c.tr_desc)
        .outerjoin(TrDescLong, TrDescLong.id == catman_swap.c.tr_desc_long)
        .outerjoin(TrMetaTitle, TrMetaTitle.id == catman_swap.c.tr_metatitle)
        .outerjoin(TrMetaDesc, TrMetaDesc.id == catman_swap.c.tr_metadesc)
        .outerjoin(catman_parent_ids,catman_parent_ids.c.child_id == catman_swap.c.id)
        .outerjoin(TrGeneratedTitle, TrGeneratedTitle.id == catman_swap.c.generated_title)
        .outerjoin(technical_branches_sq, technical_branches_sq.c.catman_id == catman_swap.c.id)
        .outerjoin(universal_branches_sq, universal_branches_sq.c.catman_id == catman_swap.c.id)
        .limit(limit)
        .offset(offset)
    )
