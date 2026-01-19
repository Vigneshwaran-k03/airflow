from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
from common.mysql_connection import get_mysql_session
from common.typesense_client import get_typesense_client
from data.service_typesense_schema import SERVICE_SCHEMA
import json

Base = declarative_base()


class SupportTicketsTypes(Base):
    __tablename__ = "support_tickets_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_admin = Column(Integer, nullable=True)
    tr_title = Column(Integer, nullable=True)
    tr_text = Column(Integer, nullable=True)
    for_particulier = Column(Boolean, default=False)
    for_station = Column(Boolean, default=False)
    for_distributeur = Column(Boolean, default=False)
    logisticFee = Column(Integer, nullable=True)
    is_reserved = Column(Boolean, default=False)
    ordre = Column(Integer, nullable=True)
    is_service = Column(Boolean, default=False)
    image = Column(String(255), nullable=True)
    id_category = Column(Integer, nullable=True)
    landing = Column(String(255), nullable=True)
    tr_nom = Column(Integer, nullable=True)
    tr_description_swap = Column(Integer, nullable=True)
    img_swap = Column(String(255), nullable=True)
    score = Column(Integer, nullable=True)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_entite = Column(Integer)
    mail = Column(String(100))
    pseudo = Column(String(100))
    commercial_cegid = Column(String(75))
    id_depot = Column(Integer)
    id_service = Column(Integer)
    id_langue = Column(String(2))
    id_devise = Column(Integer)
    environment_id = Column(Integer)
    is_developer = Column(Boolean)
    is_god = Column(Boolean)
    avatar = Column(String(150))
    background = Column(String(150))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class Translate(Base):
    __tablename__ = "translate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fr = Column(Text)
    en = Column(Text)
    es = Column(Text)
    po = Column(Text)
    de = Column(Text)
    gr = Column(Text)
    cn = Column(Text)
    ru = Column(Text)
    ne = Column(Text)
    it = Column(Text)
    pl = Column(Text)
    hu = Column(Text)
    sk = Column(Text)
    cs = Column(Text)
    hr = Column(Text)
    ro = Column(Text)
    bg = Column(Text)
    id_type = Column(Integer)
    table = Column(String(50))
    field = Column(String(50))
    target = Column(Integer)
    status = Column(Text)


def get_translation_all(session, tr_id):
    """Fetch all translations for a given translation ID."""
    if not tr_id:
        return {}

    tr = session.query(Translate).filter(Translate.id == tr_id).first()
    if not tr:
        return {}

    fields = [
        "fr",
        "en",
        "es",
        "de",
        "ru",
        "pl",
        "sk",
        "cs",
        "hr",
        "ro",
        "bg",
        "po",
        "it",
        "hu",
        "gr",
        "cn",
        "ne",
    ]

    translations = {}
    for lang in fields:
        value = getattr(tr, lang, None)
        if value:
            translations[lang] = {"title": value}
    return translations


def get_translation(session, tr_id, field_name="fr"):
    """Fetch translation text for a specific field."""
    if not tr_id:
        return ""
    tr = session.query(Translate).filter(Translate.id == tr_id).first()
    return getattr(tr, field_name, "") if tr else ""


def index_services_typesense():
    session = get_mysql_session("mysql_db")
    ts_client = get_typesense_client()

    # Ensure collection exists
    collections = [c["name"] for c in ts_client.collections.retrieve()]
    if "services" not in collections:
        ts_client.collections.create(SERVICE_SCHEMA)
        print(" Created new Typesense collection: services")
    else:
        print(" Collection 'services' already exists")

    try:
        allowed_ids = [20, 45, 44, 46, 64]
        records = (
            session.query(SupportTicketsTypes)
            .filter(SupportTicketsTypes.id.in_(allowed_ids))
            .all()
        )
        print(f"[INFO] Fetched {len(records)} records for allowed IDs: {allowed_ids}")

        documents = []
        for record in records:
            admin_data = None
            if record.id_admin and record.id_admin > 0:
                admin = session.query(Admin).filter(Admin.id == record.id_admin).first()
                if admin:
                    avatar_url = (
                        f"https://files.swap-europe.com/images/admins/avatars/{admin.avatar}"
                        if admin.avatar
                        else None
                    )
                    admin_data = {
                        "id": admin.id,
                        "entity_id": admin.id_entite,
                        "mail": admin.mail,
                        "pseudo": admin.pseudo,
                        "warehouse_id": admin.id_depot,
                        "service_id": admin.id_service,
                        "language_id": admin.id_langue,
                        "currency_id": admin.id_devise,
                        "environment_id": admin.environment_id,
                        "is_developer": bool(admin.is_developer),
                        "is_god": bool(admin.is_god),
                        "avatar_image": {
                            "folder": "/images/admins/avatars" if admin.avatar else None,
                            "file": admin.avatar or None,
                            "url": avatar_url,
                            "size": 0,
                            "type": "image/jpeg" if admin.avatar else None,
                        },
                        "background_image": {
                            "folder": "/images/admins/backgrounds"
                            if admin.background
                            else None,
                            "file": admin.background or None,
                            "url": (
                                f"https://files.swap-europe.com/images/admins/backgrounds/{admin.background}"
                                if admin.background
                                else None
                            ),
                            "size": 0,
                            "type": "image/jpeg" if admin.background else None,
                        },
                    }

            translations = get_translation_all(session, record.tr_title)
            if "fr" in translations:
                desc_fr = (get_translation(session, record.tr_text, "fr") or "").strip()
                name_fr_val = (get_translation(session, record.tr_nom, "fr") or "").strip()
                swap_desc_fr = (
                    get_translation(session, record.tr_description_swap, "fr") or ""
                ).strip()

                if desc_fr:
                    translations["fr"]["description"] = desc_fr
                if name_fr_val:
                    translations["fr"]["name"] = name_fr_val
                if swap_desc_fr:
                    translations["fr"]["swap_description"] = swap_desc_fr

            title_fr = str(get_translation(session, record.tr_title, "fr") or "")
            name_fr = str(get_translation(session, record.tr_nom, "fr") or "")
            description_fr = str(get_translation(session, record.tr_text, "fr") or "")
            swap_description = str(
                get_translation(session, record.tr_description_swap, "fr") or ""
            )

            doc = {
                "id": str(record.id),
                "admin_id": record.id_admin or 0,
                "title": title_fr,
                "description": description_fr,
                "is_for_particular": bool(record.for_particulier),
                "is_for_repairer": bool(record.for_station),
                "is_for_seller": bool(record.for_distributeur),
                "logistic_fee": record.logisticFee or 0,
                "is_reserved": bool(record.is_reserved),
                "order": record.ordre or 0,
                "is_service_ticket": bool(record.is_service),
                "image": record.image or "",
                "category_id": record.id_category or 0,
                "landing": record.landing or "",
                "name": name_fr,
                "swap_description": swap_description,
                "swap_image": record.img_swap or "",
                "admin": admin_data,
                "translations_fr": str(translations.get("fr", {})),
                "translations_en": str(translations.get("en", {})),
                "environment": ["SWAP"] if record.id in allowed_ids else [],
                "search_title": name_fr or title_fr,
            }

            documents.append(doc)
        
        output_file = "/opt/airflow/services_export.json"
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(documents, f, ensure_ascii=False, indent=4)
            print(f"[INFO] Saved {len(documents)} documents to {output_file}")
        except Exception as e:
            print(f"[ERROR] Failed to save JSON file: {e}")


        print(f"[INFO] Indexing {len(documents)} documents into Typesense...")
        import_results = ts_client.collections["services"].documents.import_(documents, {"action": "upsert"})
        for r in import_results:
            print(r) 
        print(" Bulk indexing completed successfully into Typesense!")

    except Exception as e:
        print(f"[ERROR] Failed during Typesense indexing: {e}")

    finally:
        session.close()
        print("[INFO] MySQL session closed.")


if __name__ == "__main__":
    index_services_typesense()
