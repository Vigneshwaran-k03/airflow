from sqlalchemy import select, func, cast, String
from sqlalchemy.orm import aliased
from models.products import Product, D3E, ProductMachine, Environment, EnvironmentProduct
from models.translation import Translate

def product_base_query(limit: int = None, offset: int = None):
    # Aliases for Translation Joins
    t_name = aliased(Translate, name="t_name")
    t_short_desc = aliased(Translate, name="t_short_desc")
    t_long_desc = aliased(Translate, name="t_long_desc")
    t_meta_title = aliased(Translate, name="t_meta_title")
    t_meta_desc = aliased(Translate, name="t_meta_desc")
    t_orig_refs = aliased(Translate, name="t_orig_refs")
    
    # query
    stmt = select(
        Product.id,
        Product.type,
        Product.code_douane.label('customs_code'),
        Product.ref,
        Product.poids.label('weight'),
        Product.code_barres.label('barcode'),
        Product.commentaire.label('comment'),
        
        # Translation: tr_nom -> name
        cast(func.json_object(*Translate.json_args(t_name)), String).label('name'),
        
        # Translation: generated_short_description -> short_description
        cast(func.json_object(*Translate.json_args(t_short_desc)), String).label('short_description'),
        
        # Translation: generated_long_description -> long_description
        cast(func.json_object(*Translate.json_args(t_long_desc)), String).label('long_description'),
        
        Product.is_visible,
        Product.is_obsolete,
        
        # img -> image
        Product.img.label('image'),
        
        Product.hscode.label('hs_code'),

        #brand
        Product.id_marque.label('brand'),
        
        # Translation: generated_meta_title -> meta_title
        cast(func.json_object(*Translate.json_args(t_meta_title)), String).label('meta_title'),
        
        # Translation: generated_meta_description -> meta_description
        cast(func.json_object(*Translate.json_args(t_meta_desc)), String).label('meta_description'),
        
        # Translation: generated_original_references -> original_references
        cast(func.json_object(*Translate.json_args(t_orig_refs)), String).label('original_references'),
        
        # generated_url -> url (Assuming it contains a JSON string or similar that needs parsing)
        Product.swapUrl.label('url'),

        #d3e
        cast(
        func.json_object(
        "id", D3E.id,
        "company_id", D3E.id_societe,
        "name", D3E.nom,
        "price", D3E.prix
        ), String
        ).label("d3e"),

        #Machine
        cast(
        func.json_object(
        "id", ProductMachine.id,
        "supplier_id", ProductMachine.id_fournisseur,
        "supplier_reference", ProductMachine.ref_usine,
        "repair_score", ProductMachine.repair_score,
        "buying_price", ProductMachine.prix_achat,
        "pricing_discount_a", ProductMachine.tarif_remise_a,
        "pricing_discount_a_a", ProductMachine.tarif_remise_aa,
        "pricing_discount_b", ProductMachine.tarif_remise_b,
        "pricing_discount_c", ProductMachine.tarif_remise_c,
        "permanent_p_p_i", ProductMachine.PPI_permanent,
        "observed_public_price", ProductMachine.PPI_promo,
        "cegid_d_p_r", ProductMachine.dpr_cegid,
        "real_d_p_r", ProductMachine.dpr_reel,
        "is_motor", ProductMachine.is_motor,
        "is_repair_forbidden", ProductMachine.is_repair_forbidden,
        "return_rate", ProductMachine.return_rate,
        "max_return_rate", ProductMachine.max_return_rate,
        "exploded_view", ProductMachine.vue_eclatee,
        "universal_branch", ProductMachine.id_arborescence
        ), String
        ).label("machine"),




    ).select_from(Product)

    # Joins
    stmt = stmt.outerjoin(t_name, Product.tr_nom == t_name.id)
    stmt = stmt.outerjoin(t_short_desc, Product.generated_short_description == t_short_desc.id)
    stmt = stmt.outerjoin(t_long_desc, Product.generated_long_description == t_long_desc.id)
    stmt = stmt.outerjoin(t_meta_title, Product.generated_meta_title == t_meta_title.id)
    stmt = stmt.outerjoin(t_meta_desc, Product.generated_meta_description == t_meta_desc.id)
    stmt = stmt.outerjoin(t_orig_refs, Product.generated_original_references == t_orig_refs.id)
    stmt = stmt.outerjoin(D3E, Product.id_d3e == D3E.id)
    stmt = stmt.outerjoin(ProductMachine, Product.id_machine == ProductMachine.id)

    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    return stmt
