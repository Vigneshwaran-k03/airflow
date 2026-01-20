from sqlalchemy import select, table, column, cast, func, String, literal
from sqlalchemy.orm import aliased
from models.translation import Translate

tarifs = table(
    "tarifs",
    column("id"),
    column("id_societe"),
    column("id_vio_machine"),
    column("tr_nom"),
    column("code"),
    column("debut"),
    column("fin"),
    column("reduc"),
    column("is_franco"),
    column("francoThreshold"),
    column("is_enabled"),
    column("produits"),
    column("entites"),
    column("is_all_produits"),
    column("is_all_entites"),
    column("is_shop"),
    column("is_overriding_fixed_price"),
    column("query"),
    column("products_threshold"),
)
#table of company details 
societes = table(
    "societes",
    column("id"),
    column("id_entite"),
    column("api_mail"),
    column("nom"),
    column("adresse"),
    column("cp"),
    column("ville"),
    column("id_pays"),
    column("tel"),
    column("tel_eshop"),
    column("mail"),
    column("fax"),
    column("tva"),
    column("capital"),
    column("code_eori"),
)
#environment table 
environment = table(
    "environment",
    column("label"),
)


def pricing_environment_query():
    """
    Query to get all environment labels for each pricing/tarif.
    Returns all environment labels as a JSON array.
    """
    return (
        select(
            # Return all environment labels as JSON array
            func.coalesce(
                func.json_arrayagg(
                    environment.c.label
                ),
                func.json_array()
            ).label("environment"),
        )
        .select_from(environment)
    )


def pricing_base_query(limit=None, offset=None):
    """
    Query the tarifs table with translations for the name field and company details.
    """
    TrName = aliased(Translate)
    env_subq = pricing_environment_query().subquery("pricing_env")

    return (
        select(
            # Primary fields
            tarifs.c.id.label("id"),
            tarifs.c.id_societe.label("company_id"),
            tarifs.c.id_vio_machine.label("vio_machine_id"),
            tarifs.c.id_vio_machine.label("vio_machine"),
            tarifs.c.code.label("code"),
            tarifs.c.reduc.label("reduction"),
            
            # Boolean/flag fields
            tarifs.c.is_franco.label("has_free_shipping"),
            tarifs.c.is_enabled.label("is_enabled"),
            tarifs.c.is_all_produits.label("has_all_products"),
            tarifs.c.is_all_entites.label("has_all_entities"),
            tarifs.c.is_shop.label("is_shop"),
            tarifs.c.is_overriding_fixed_price.label("is_overriding_fixed_price"),
            
            # Threshold and enum fields
            tarifs.c.francoThreshold.label("free_shipping_threshold"),
            tarifs.c.products_threshold.label("products_threshold"),
            tarifs.c.produits.label("products_type"),
            tarifs.c.entites.label("entities_type"),
            tarifs.c.query.label("query"),

            # Dates (DATE only, no timezone)
            cast(tarifs.c.debut, String).label("start_date"),
            cast(tarifs.c.fin, String).label("end_date"),
            
            # Environment array
            env_subq.c.environment.label("environment"),
            
            # Translation (JSON as STRING - flattened later)
            cast(func.json_object(*Translate.json_args(table=TrName)), String).label("name"),
            
            # Company details as JSON object
            cast(
                func.json_object(
                    "id", societes.c.id,
                    "entity_id", societes.c.id_entite,
                    "api_mail", societes.c.api_mail,
                    "name", societes.c.nom,
                    "address", societes.c.adresse,
                    "zip_code", societes.c.cp,
                    "city", societes.c.ville,
                    "country_id", societes.c.id_pays,
                    "tel", societes.c.tel,
                    "tel_eshop", societes.c.tel_eshop,
                    "mail", societes.c.mail,
                    "fax", societes.c.fax,
                    "tax_rate", societes.c.tva,
                    "capital", societes.c.capital,
                    "eori_code", societes.c.code_eori,
                ),
                String
            ).label("company"),
        )
        .outerjoin(TrName, TrName.id == tarifs.c.tr_nom)
        .outerjoin(societes, societes.c.id == tarifs.c.id_societe)
        .outerjoin(env_subq, env_subq.c.environment.isnot(None))
        .limit(limit)
        .offset(offset)
    )
