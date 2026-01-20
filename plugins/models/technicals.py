from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Technical(Base):
    __tablename__ = "arbre_kit_technique"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_parent = Column(Integer)
    
    # Translation Foreign Keys
    nom = Column(Integer)
    label = Column(Integer)
    
    poids = Column(DECIMAL(10, 2))
    is_consommable = Column(Boolean, default=False)
    is_accessory = Column(Boolean, default=False)
    is_other = Column(Boolean, default=False)
    conditionnement = Column(String(255))
    is_visible = Column(Boolean, default=True)
    img = Column(String(255))
    hs_code = Column(String(50))
    score = Column(Integer)

class TechnicalParentIds(Base):
    __tablename__ = "tech_parent_ids"
    
    id = Column(Integer, primary_key=True)
    parent_ids = Column(Text)
