from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Universal(Base):
    __tablename__ = "arborescence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_parent = Column(Integer)
    id_d3e = Column(Integer)
    
    # Translation Foreign Keys
    tr_nom = Column(Integer)
    tr_label = Column(Integer)
    tr_sommaire = Column(Integer)
    tr_alias = Column(Integer)
    
    img = Column(String(255))
    default_machine_img = Column(String(255))
    background = Column(String(255))
    icon = Column(String(255))
    
    code_douane = Column(String(50))
    poids_moyen = Column(DECIMAL(10, 2))
    has_battery = Column(Boolean, default=False)
    depreciation_rate = Column(DECIMAL(10, 2))
    is_visible_front = Column(Boolean, default=True)


class UniversalParentIds(Base):
    __tablename__ = "arborescence_parent_ids"
    
    id = Column(Integer, primary_key=True)
    parent_ids = Column(Text)