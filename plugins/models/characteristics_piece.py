from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, Text, Enum, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

#characteristic table
class Characteristic(Base):
    __tablename__ = "characteristic"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer, nullable=True)
    technical_branch_id = Column(Integer, nullable=True)
    type = Column(Enum('boolean','enum','unit'), nullable=False)
    unit_id = Column(Integer, nullable=True)

#characteristic_piece_value table
class characteristic_piece_value(Base):
    __tablename__ = "characteristic_piece_value"

    id = Column(Integer, primary_key=True, autoincrement=True)
    piece_id = Column(Integer, nullable=False)
    characteristic_id = Column(Integer, nullable=False)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)
    boolean_value = Column(Boolean, nullable=True)
    enum_value_id = Column(Integer, nullable=True)
    environment_id = Column(Integer, nullable=True)
    environment_exclusion = Column(Boolean, nullable=False, default=False)
   
#Unit table
class Unit(Base):
    __tablename__ = "characteristic_unit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer, nullable=True)
    symbol = Column(String(32), nullable=True)
    type_id = Column(Integer, nullable=True)

   