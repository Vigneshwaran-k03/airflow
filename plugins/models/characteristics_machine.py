from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text, Enum, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

#caracteristiques machine

class CharacteristicMachine(Base):
    __tablename__ = "caracteristiques"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_unit = Column(Integer, nullable=True)
    tr_nom = Column(Integer, nullable=True)
    img = Column(String(100), nullable=True)
    est_un_selecteur = Column(Boolean, nullable=False)

#l_caracteristiques_produits

class CharacteristicProduct(Base):
    __tablename__ = "l_caracteristiques_produits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_produit = Column(Integer, nullable=True)
    id_caracteristique = Column(Integer, nullable=True)
    value = Column(String(255), nullable=True)
    in_name = Column(Boolean, nullable=False)
    ordre = Column(Integer, nullable=True)
    environment_id = Column(Integer, nullable=True)
    environment_exclusion = Column(Boolean, nullable=False)
    ts_creation = Column(DateTime, nullable=False)
    environment = Column(String(32), nullable=True)

#unit

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_type = Column(Integer, nullable=True)
    tr_nom = Column(Integer, nullable=True)
    unit = Column(String(20), nullable=True)
    tr_unit = Column(Integer, nullable=True)

#units type
class UnitType(Base):
    __tablename__ = "units_types"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tr_nom = Column(Integer, nullable=True)
    is_text = Column(Boolean, nullable=True)
    is_enum = Column(Boolean, nullable=True)
    is_boolean = Column(Boolean, nullable=True)