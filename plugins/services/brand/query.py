from sqlalchemy import select, func, cast, String, table, column, distinct
from sqlalchemy.orm import aliased

from models.brands import Marques, MarquesAlias
from models.translation import Translate

def brands_base_query( limit: int = None, offset: int = None):
    """
    Base SELECT for brands.
    Polars-safe: all JSON / GROUP_CONCAT cast to STRING.
    """

    TranslateTitle = aliased(Translate)
    TranslateDesc = aliased(Translate)
    TranslateLongDesc = aliased(Translate)
    TranslateMeta = aliased(Translate)
    TranslateDescB2B = aliased(Translate)

    return (
        select(
            Marques.id.label("id"),
            Marques.nom.label("name"),
            Marques.alias,
            Marques.is_main,
            Marques.is_seller.label("is_seller_brand"),
            Marques.is_show_part_brand_search,
            Marques.is_visible,
            Marques.has_parts,
            Marques.lien.label("link"),
            cast(
                func.json_object(*Translate.json_args(table=TranslateTitle)),
                String,
            ).label("title"),

            cast(
                func.json_object(*Translate.json_args(table=TranslateDesc)),
                String,
            ).label("description"),

            cast(
                func.json_object(*Translate.json_args(table=TranslateLongDesc)),
                String,
            ).label("long_description"),

            cast(
                func.json_object(*Translate.json_args(table=TranslateMeta)),
                String,
            ).label("meta"),

            cast(
                func.json_object(*Translate.json_args(table=TranslateDescB2B)),
                String,
            ).label("description_b2b"),

            Marques.background_site.label("background_image"),
            Marques.is_origine.label("is_origin"),
            Marques.image,
            cast(
                func.group_concat(func.distinct(MarquesAlias.alias)),
                String,
            ).label("aliases"),
            func.concat(Marques.nom, ' ', Marques.alias, ' ', func.group_concat(func.distinct(MarquesAlias.alias))).label("search_title"),
        )
        .select_from(Marques)
        .outerjoin(MarquesAlias, MarquesAlias.brand_id == Marques.id)
        .outerjoin(TranslateTitle, TranslateTitle.id == Marques.tr_title)
        .outerjoin(TranslateDesc, TranslateDesc.id == Marques.tr_text)
        .outerjoin(TranslateLongDesc, TranslateLongDesc.id == Marques.tr_text_2)
        .outerjoin(TranslateMeta, TranslateMeta.id == Marques.tr_meta_text)
        .outerjoin(TranslateDescB2B, TranslateDescB2B.id == Marques.tr_description_b2b)
        .group_by(
            Marques.id,
            Marques.nom,
            Marques.alias,
            Marques.is_main,
        )
        .limit(limit)
        .offset(offset)
    )

def brands_environment_query(ids: list[int] = None):
    environment_product = table(
        "#environment_product",
        column("product_id"),
        column("environment_id"),
    )

    produits = table(
        "produits",
        column("id"),
        column("id_marque"),
    )

    environment = table(
        "environment",
        column("id"),
        column("label"),
    )       
    
    return (
        select(
            produits.c.id_marque.label("id"),
            func.group_concat(environment.c.label.distinct()).label("environment")
        )
        .select_from(
            environment_product
            .join(produits, produits.c.id == environment_product.c.product_id)
            .join(environment, environment.c.id == environment_product.c.environment_id)
        )
        .where(
            produits.c.id_marque.in_(ids) if ids is not None else True
        )
        .group_by(produits.c.id_marque)
    )
    