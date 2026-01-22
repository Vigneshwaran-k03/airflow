from sqlalchemy import Column, Integer, String, Float, Text, Boolean, TIMESTAMP, Enum, Numeric
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Enum('','MACHINE','KIT','PART'), default='')
    id_machine = Column(Integer, nullable=False)
    id_piece = Column(Integer, nullable=False)
    id_colisage = Column(Integer, nullable=False)
    id_referencement = Column(Integer, nullable=False)
    id_marque = Column(Integer, nullable=False)
    id_affichage = Column(Integer, nullable=False, default=2)
    id_verdun = Column(Integer, nullable=False)
    id_d3e = Column(Integer, nullable=False)
    code_douane = Column(String(50), nullable=False)
    ref = Column(String(50), nullable=False, unique=True)
    poids = Column(Float, nullable=False)
    code_barres = Column(String(13), nullable=False)
    is_ean_ok = Column(Boolean, nullable=False, default=True)
    commentaire = Column(Text, nullable=False)
    
    # Translation IDs
    tr_nom = Column(Integer, nullable=False)
    tr_descriptif = Column(Integer, nullable=False)
    tr_desc_btob = Column(Integer, nullable=False)
    tr_desc_btoc_courte = Column(Integer, nullable=False)
    tr_desc_btoc_longue = Column(Integer, nullable=False)
    tr_caracteristiques = Column(Integer, nullable=False)
    tr_utilisation = Column(Integer, nullable=False)
    tr_plus_produit = Column(Integer, nullable=False)
    tr_packaging = Column(Integer, nullable=False, default=0)
    tr_plus_conso = Column(Integer, nullable=False)
    tr_desc_courte_marketplace = Column(Integer, nullable=False)
    
    is_visible = Column(Integer, nullable=False)
    is_visible_jr = Column(Integer, nullable=False, default=0)
    is_obsolete = Column(Integer, nullable=False)
    is_useless = Column(Integer, nullable=False)
    is_useful = Column(Integer, nullable=False)
    is_vendable = Column(Integer, nullable=False)
    is_garantie = Column(Integer, nullable=False, default=1)
    
    img = Column(String(200), nullable=False)
    img_old = Column(String(200), nullable=False)
    ts_creation = Column(Integer, nullable=False)
    
    stock_mini = Column(Integer, nullable=False, default=2)
    stock_maxi = Column(Integer, nullable=False, default=10)
    dpr = Column(Float, nullable=False)
    stock_mini_temp = Column(Integer, nullable=False, default=99999999)
    
    swapUrl = Column(String(250), nullable=False, unique=True)
    swapUrlModeration = Column(TIMESTAMP, nullable=True)
    
    generation_nom_auto = Column(Boolean, nullable=False, default=False)
    lien_qrcode = Column(Text, nullable=False)
    stored_name = Column(Integer, nullable=True)
    
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    id_produit_origine = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=False, default=0)
    hscode = Column(String(32), nullable=True)
    
    generated_name = Column(Integer, nullable=True)
    generated_short_description = Column(Integer, nullable=True)
    generated_long_description = Column(Integer, nullable=True)
    generated_meta_title = Column(Integer, nullable=True)
    generated_meta_description = Column(Integer, nullable=True)
    generated_original_references = Column(Integer, nullable=True)
    generated_url = Column(String(255), nullable=True)
    
    score = Column(Integer, nullable=False, default=0)
    tr_conseil_reparation = Column(Integer, nullable=True)
    nameplate_details = Column(String(255), nullable=True)
class d3e(Base):
    __tablename__ = "d3e"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_societe=Column(Integer,nullable=True)
    nom=Column(String(50),nullable=True)
    prix = Column(Numeric(6, 2), nullable=True)
    