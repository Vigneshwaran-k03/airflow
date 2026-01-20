from sqlalchemy import select
from models.translation import Translate

def teract_translations_query(limit: int = None, offset: int = None):
    query = select(
        Translate.id,
        Translate.fr,
        Translate.en,
        Translate.es,
        Translate.po,
        Translate.de,
        Translate.gr,
        Translate.cn,
        Translate.ru,
        Translate.ne,
        Translate.it,
        Translate.pl,
        Translate.hu,
        Translate.sk,
        Translate.cs,
        Translate.hr,
        Translate.ro,
        Translate.bg,
        Translate.id_type,
        Translate.table,
        Translate.field,
        Translate.target,
        Translate.status
    ).where(Translate.id_type == 23)

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
        
    return query
