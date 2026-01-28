from sqlalchemy import Column, Integer, String, Float, Text, Boolean, TIMESTAMP, Enum, Numeric, Date
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

#d3e
class D3E(Base):
    __tablename__ = "d3e"

    id = Column(Integer, primary_key=True)
    id_societe = Column(Integer, nullable=False)
    nom = Column(String(50), nullable=False)
    prix = Column(Numeric(6, 2), nullable=False)
    is_main = Column(Boolean, nullable=False)


#machine 
class ProductMachine(Base):
    __tablename__ = "f_produits_machine"

    id = Column(Integer, primary_key=True)
    id_produit = Column(Integer, unique=True, nullable=False)
    id_fournisseur = Column(Integer, nullable=False)
    id_arborescence = Column(Integer, nullable=False)
    ref_usine = Column(String(50), nullable=False)
    repair_score = Column(Numeric(5,2))
    prix_achat = Column(Numeric(10,2))
    tarif_remise_a = Column(Numeric(10,2))
    tarif_remise_aa = Column(Numeric(10,2))
    tarif_remise_b = Column(Numeric(10,2))
    tarif_remise_c = Column(Numeric(10,2))
    PPI_permanent = Column(Numeric(10,2))
    PPI_promo = Column(Numeric(10,2))
    dpr_cegid = Column(Numeric(10,2))
    dpr_reel = Column(Numeric(10,2))
    vue_eclatee = Column(String(150))
    is_motor = Column(Boolean)
    is_repair_forbidden = Column(Boolean)
    return_rate = Column(Numeric(5,2))
    max_return_rate = Column(Numeric(5,2))

#Piece
class ProductPiece(Base):
    __tablename__ = "f_produits_piece"

    id = Column(Integer, primary_key=True)
    prix_swap = Column(Numeric(10, 2), nullable=False)
    isLocked = Column(Boolean, nullable=False)
    is_consommable = Column(Boolean, nullable=False)
    is_alaune = Column(Boolean, nullable=False)
    forcedSale = Column(Integer, nullable=False)
    isForced = Column(Boolean, nullable=False, default=True)
    is_origine = Column(Boolean, nullable=False, default=True)
    id_branche_technique = Column(Integer, nullable=True)

#Parts
class PieceParts(Base):
    __tablename__ = "l_pieces_parts"

    id_piece = Column(Integer, primary_key=True, nullable=False)
    id_part = Column(Integer, primary_key=True, nullable=False)
    qte = Column(Integer, nullable=False, default=1)


#for extensions
class Environment(Base):
    __tablename__ = "environment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=True)
    society_id = Column(Integer, nullable=True)
    label = Column(String(45), nullable=False, unique=True)
    name = Column(String(45), nullable=True)
    nature = Column(Enum('root','eshop','collect','vitrine'), nullable=False)
    tax_rate = Column(Numeric(5, 2), nullable=False, default=0.00)
    is_locked = Column(Integer, nullable=False, default=0)
    use_linked_products = Column(Boolean, nullable=True, default=False)
    logo = Column(String(128), nullable=True)
    favicon = Column(String(128), nullable=True)
    home_image = Column(String(255), nullable=True)
    home_image_link = Column(String(255), nullable=True)
    contact_tel = Column(String(32), nullable=True)
    service_tel = Column(String(32), nullable=True)
    primary_color = Column(String(7), nullable=True)
    secondary_color = Column(String(7), nullable=True)
    tertiary_color = Column(String(7), nullable=True)
    title_font = Column(String(64), nullable=True)
    text_font = Column(String(64), nullable=True)
    repair_category_id = Column(Integer, nullable=True)
    top_sales_category_id = Column(Integer, nullable=True)
    refurbished_category_id = Column(Integer, nullable=True)
    gtm_identifier = Column(String(45), nullable=True)
    url_pattern = Column(String(255), nullable=True)
    promo_banner_data = Column(Text, nullable=True)  # Json
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class LEnvironmentProduct(Base):
    __tablename__ = "l_environment_product"

    environment_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    reference = Column(String(50), nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    price_promo = Column(Numeric(10, 2), nullable=True)
    discount_start_date = Column(Date, nullable=True)
    discount_end_date = Column(Date, nullable=True)
    currency_id = Column(Integer, nullable=True, default=1)
    is_visible = Column(Boolean, nullable=True)
    forced_sale = Column(Integer, nullable=True)
    is_price_forced = Column(Boolean, nullable=True)
    url = Column(String(250), nullable=True)
    tr_meta_title = Column(Integer, nullable=True)
    tr_meta_description = Column(Integer, nullable=True)
    tr_description_short = Column(Integer, nullable=True)
    tr_description_long = Column(Integer, nullable=True)
    tr_specifics = Column(Integer, nullable=True)
    tr_original_references = Column(Integer, nullable=True)
    tr_product_name = Column(Integer, nullable=True)
    img = Column(String(255), nullable=True)
    score = Column(Integer, nullable=True)
    fixed_columns = Column(Integer, nullable=False, default=0)
    moderated_at = Column(TIMESTAMP, nullable=True)
    modified_at = Column(TIMESTAMP, nullable=True, onupdate=func.current_timestamp())
    is_calculation_avoided = Column(Integer, nullable=True, default=0)
    review_count = Column(Integer, nullable=True)
    average_rating = Column(Float, nullable=True)
    default_category_id = Column(String(45), nullable=True)

#categories
class Category(Base):
    __tablename__ = "catman_product"

    catman_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    order = Column(Integer, nullable=True)

#Machines and Pieces
class Machines_and_Pieces(Base):
    __tablename__ = "l_machines_pieces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_machine = Column(Integer, nullable=False)
    id_piece = Column(Integer, nullable=False)

