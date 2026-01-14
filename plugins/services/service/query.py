from sqlalchemy import select, func, cast, String, table, column
from sqlalchemy.orm import aliased

from models.service_to_typesense import SupportTicketsTypes, Admin
from models.translation import Translate

def services_base_query(limit: int = None, offset: int = None):
    """
    Base SELECT for service.
    Polars-safe: all JSON / GROUP_CONCAT cast to STRING.
    """

    TranslateTitle = aliased(Translate)
    TranslateText = aliased(Translate)
    TranslateName = aliased(Translate)
    TranslateSwapDesc = aliased(Translate)
    allowed_ids = [20, 45, 44, 46, 64] # allowed these IDs


    return (
        select(
            SupportTicketsTypes.id.label("id"),
            SupportTicketsTypes.id_admin.label("admin_id"),
            cast(
                func.json_object(*Translate.json_args(table=TranslateTitle)),
                String,
            ).label("title"),
            cast(
                func.json_object(*Translate.json_args(table=TranslateText)),
                String,
            ).label("description"),
            cast(
                func.json_object(*Translate.json_args(table=TranslateName)),
                String,
            ).label("name"),
            cast(
                func.json_object(*Translate.json_args(table=TranslateSwapDesc)),
                String,
            ).label("swap_description"),
            SupportTicketsTypes.for_particulier.label("is_for_particular"),
            SupportTicketsTypes.for_station.label("is_for_repairer"),
            SupportTicketsTypes.for_distributeur.label("is_for_seller"),
            SupportTicketsTypes.logisticFee.label("logistic_fee"),
            SupportTicketsTypes.is_reserved.label("is_reserved"),
            SupportTicketsTypes.ordre.label("order"),
            SupportTicketsTypes.is_service.label("is_service_ticket"),
            SupportTicketsTypes.image,
            SupportTicketsTypes.id_category.label("category_id"),
            SupportTicketsTypes.landing,
            SupportTicketsTypes.img_swap.label("swap_image"),
            SupportTicketsTypes.score,
        )
        .select_from(SupportTicketsTypes)
        .outerjoin(TranslateTitle, TranslateTitle.id == SupportTicketsTypes.tr_title)
        .outerjoin(TranslateText, TranslateText.id == SupportTicketsTypes.tr_text)
        .outerjoin(TranslateName, TranslateName.id == SupportTicketsTypes.tr_nom)
        .outerjoin(TranslateSwapDesc, TranslateSwapDesc.id == SupportTicketsTypes.tr_description_swap)
        .where(SupportTicketsTypes.id.in_(allowed_ids))
        .limit(limit)
        .offset(offset)
    )


def services_admin_query(admin_ids: list[int] = None):
    """
    Fetch admin details for service.
    """
    query = select(
        Admin.id.label("id"),
        Admin.id_entite.label("entity_id"),
        Admin.mail,
        Admin.pseudo,
        Admin.id_depot.label("warehouse_id"),
        Admin.id_service.label("service_id"),
        Admin.id_langue.label("language_id"),
        Admin.id_devise.label("currency_id"),
        Admin.environment_id,
        Admin.is_developer,
        Admin.is_god,
        Admin.avatar,
        Admin.background,
    )

    if admin_ids:
        query = query.where(Admin.id.in_(admin_ids))

    return query
