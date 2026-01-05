from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy import inspect

Base = declarative_base()

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
    status = Column(String)

    @classmethod
    def translation_columns(cls):
        """Return all columns that are actual translations."""
        exclude_cols = {"id", "id_type", "table", "field", "target", "status"}
        return [c.name for c in inspect(cls).c if c.name not in exclude_cols]

    @classmethod
    def json_args(cls, table=None):
        """
        Return list suitable for func.json_object(*args).
        Accepts aliased table or base table.
        """
        args = []

        # Determine the table to use
        if table is None:
            table_to_use = cls.__table__
            for col in cls.translation_columns():
                args.extend([col, getattr(table_to_use.c, col)])
        else:
            # Aliased ORM object
            for col in cls.translation_columns():
                args.extend([col, getattr(table, col)])

        return args

    @classmethod
    def normalize_translations(cls, raw_value):
        """
        Normalize translations globally.

        Rules:
        - Auto-detect languages from model
        - fr & en always exist (fallback to fallback_value)
        - Remove empty translations
        - Accept dict or JSON string
        """
        languages = cls.translation_columns()

        data = {}

        if raw_value:
            if isinstance(raw_value, dict):
                data = raw_value
            else:
                try:
                    parsed = json.loads(raw_value)
                    if isinstance(parsed, dict):
                        data = parsed
                except Exception:
                    pass

        cleaned = {}

        for lang in languages:
            val = data.get(lang)

            if val and str(val).strip():
                cleaned[lang] = str(val).strip()

        return cleaned or {}
    