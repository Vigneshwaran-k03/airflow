from sqlalchemy import select, func, cast, String, case
from sqlalchemy.orm import aliased
from models.products import (Product,
 D3E, 
 ProductMachine, 
 Environment, 
 LEnvironmentProduct, 
 Category,
 ProductPiece,
 Machines_and_Pieces,
 PieceParts,
 Packaging,
 Document,
 DocumentType,
 EnvironmentProduct,
 tarifs,
 Stock,
 Depot,
 CharacteristicMachine,
 caracteristiques,
 units,
 UnitsTypes,
 characteristic_piece_value,
 characteristic,
 characteristic_enum,
 UnitsTypes,
 suppliers,
 ot_links,
 ot_colis,
 ot_commandes,
 ot_commandes,
 Images,
 Accessories,
 Accessories,
 Alternatives,
 Videos,
 Alias,
 AliasCategories,
 EnvironmentProductField,
 EnvironmentProductImage
 )
from models.translation import Translate
from models.universals import Universal

def product_base_query(limit: int = None, offset: int = None):
    # Aliases for Translation Joins (Main Product)
    t_name = aliased(Translate, name="t_name")
    t_short_desc = aliased(Translate, name="t_short_desc")
    t_long_desc = aliased(Translate, name="t_long_desc")
    t_meta_title = aliased(Translate, name="t_meta_title")
    t_meta_desc = aliased(Translate, name="t_meta_desc")
    t_orig_refs = aliased(Translate, name="t_orig_refs")
    
    # Aliases for Translation Joins (Extensions)
    t_ext_name = aliased(Translate, name="t_ext_name")
    t_ext_meta_title = aliased(Translate, name="t_ext_meta_title")
    t_ext_meta_desc = aliased(Translate, name="t_ext_meta_desc")
    t_ext_short_desc = aliased(Translate, name="t_ext_short_desc")
    t_ext_long_desc = aliased(Translate, name="t_ext_long_desc")
    t_ext_specifics = aliased(Translate, name="t_ext_specifics")
    t_ext_orig_refs = aliased(Translate, name="t_ext_orig_refs")

    # Alias for Document Environment
    DocEnv = aliased(Environment, name="doc_env")

    # Alias for enum translation
    t_enum = aliased(Translate, name="t_enum")

    # Alias for Video Title Translation
    t_video_title = aliased(Translate, name="t_video_title")

    # Aliases for D3E logic
    d3e_direct = aliased(D3E, name="d3e_direct")
    d3e_fallback = aliased(D3E, name="d3e_fallback")
    universal_fallback = aliased(Universal, name="universal_fallback")

    # Base price expression for pricing
    base_price_expr = func.coalesce(
        LEnvironmentProduct.price,
        ProductPiece.prix_swap
    )


    # Subquery for Extensions
    extensions_subquery = (
        select(
            func.json_arrayagg(
                func.json_object(
                    "label", Environment.label,
                    "data", func.json_object(
                        "reference", LEnvironmentProduct.reference,
                        "price", LEnvironmentProduct.price,
                        "discount_price", LEnvironmentProduct.price_promo,
                        "discount_start_date", LEnvironmentProduct.discount_start_date,
                        "discount_end_date", LEnvironmentProduct.discount_end_date,
                        "currency_id", LEnvironmentProduct.currency_id,
                        "is_visible", LEnvironmentProduct.is_visible,
                        "forced_sale_duration", LEnvironmentProduct.forced_sale,
                        "has_forced_price", LEnvironmentProduct.is_price_forced,
                        "url", LEnvironmentProduct.url,
                        "score", LEnvironmentProduct.score,
                        "review_count", LEnvironmentProduct.review_count,
                        "average_rating", LEnvironmentProduct.average_rating,
                        "default_category_id", LEnvironmentProduct.default_category_id,
                        "img", LEnvironmentProduct.img, # Will be parsed in transformations
                        
                        # Translations
                        "name", cast(func.json_object(*Translate.json_args(t_ext_name)), String),
                        "meta_title", cast(func.json_object(*Translate.json_args(t_ext_meta_title)), String),
                        "meta_description", cast(func.json_object(*Translate.json_args(t_ext_meta_desc)), String),
                        "short_description", cast(func.json_object(*Translate.json_args(t_ext_short_desc)), String),
                        "long_description", cast(func.json_object(*Translate.json_args(t_ext_long_desc)), String),
                        "specificities", cast(func.json_object(*Translate.json_args(t_ext_specifics)), String),
                        "original_references", cast(func.json_object(*Translate.json_args(t_ext_orig_refs)), String),

                        # Calculated info needed for logic (like Tax Rate)
                         "tax_rate", Environment.tax_rate,

                        "custom_fields", func.coalesce(
                            select(func.json_objectagg(EnvironmentProductField.name, EnvironmentProductField.value))
                            .where(EnvironmentProductField.product_id == LEnvironmentProduct.product_id)
                            .where(EnvironmentProductField.environment_id == LEnvironmentProduct.environment_id)
                            .correlate(LEnvironmentProduct)
                            .scalar_subquery(),
                            func.json_object()
                        ),
                        "images", func.coalesce(
                            select(func.json_arrayagg(EnvironmentProductImage.image_id))
                            .where(EnvironmentProductImage.product_id == LEnvironmentProduct.product_id)
                            .where(EnvironmentProductImage.environment_id == LEnvironmentProduct.environment_id)
                            .correlate(LEnvironmentProduct)
                            .scalar_subquery(),
                            func.json_array()
                        )
                    )
                )
            )
        )
        .select_from(LEnvironmentProduct)
        .join(Environment, LEnvironmentProduct.environment_id == Environment.id)
        .outerjoin(t_ext_name, LEnvironmentProduct.tr_product_name == t_ext_name.id)
        .outerjoin(t_ext_meta_title, LEnvironmentProduct.tr_meta_title == t_ext_meta_title.id)
        .outerjoin(t_ext_meta_desc, LEnvironmentProduct.tr_meta_description == t_ext_meta_desc.id)
        .outerjoin(t_ext_short_desc, LEnvironmentProduct.tr_description_short == t_ext_short_desc.id)
        .outerjoin(t_ext_long_desc, LEnvironmentProduct.tr_description_long == t_ext_long_desc.id)
        .outerjoin(t_ext_specifics, LEnvironmentProduct.tr_specifics == t_ext_specifics.id)
        .outerjoin(t_ext_orig_refs, LEnvironmentProduct.tr_original_references == t_ext_orig_refs.id)
        .where(LEnvironmentProduct.product_id == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )
    # Subquery for categories
    categories_subquery = (
    select(
        func.json_arrayagg(Category.catman_id)
    )
    .where(Category.product_id == Product.id)
    .correlate(Product)
    .scalar_subquery()
    )    
    # Subquery for pieces
    pieces_from_machine_subquery = (
        select(func.json_arrayagg(Machines_and_Pieces.id_piece))
        .where(Machines_and_Pieces.id_machine == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )
    # Subquery for machines
    machines_from_piece_subquery = (
        select(func.json_arrayagg(Machines_and_Pieces.id_machine))
        .where(Machines_and_Pieces.id_piece == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    # Subquery for parts
    parts_from_piece_subquery = (
        select(func.json_arrayagg(PieceParts.id_part))
        .where(PieceParts.id_piece == Product.id_piece)
        .where(Product.id_piece > 0)
        .correlate(Product)
        .scalar_subquery()
    )
    # Subquery for documents
    documents_subquery = (
        select(
            func.json_arrayagg(
                func.json_object(
                    "id", Document.id,
                    "language_id", Document.id_langue,
                    "type_id", Document.id_type,
                    "file", Document.file,
                    "name", Document.name,
                    "order", Document.order,
                    "name", Document.name,
                    "order", Document.order,
                    "environment", DocEnv.label,
                    "dossier", DocumentType.dossier
                )
            )
        )
        .select_from(Document)
        .outerjoin(DocEnv, Document.environment_id == DocEnv.id)
        .outerjoin(DocumentType, Document.id_type == DocumentType.id)
        .where(Document.id_machine == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    # Subquery for environment
    environment_subquery = (
        select(func.json_arrayagg(Environment.label))
        .select_from(EnvironmentProduct)
        .join(Environment, EnvironmentProduct.environment_id == Environment.id)
        .where(EnvironmentProduct.product_id == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )
    
    # Subquery for pricing
    pricing_subquery = (
    select(
        func.json_objectagg(
            cast(tarifs.id, String),  # key → tariff id
            func.round(
                base_price_expr * (1 - (tarifs.reduc / 100)),
                2
            )
        )
    )
    .select_from(tarifs)
    .outerjoin(
        LEnvironmentProduct,
        LEnvironmentProduct.product_id == Product.id
    )
    .outerjoin(
        ProductPiece,
        ProductPiece.id == Product.id_piece
    )
    .where(
        (tarifs.debut == None) | (tarifs.debut <= func.now())
    )
    .where(
        (tarifs.fin == None) | (tarifs.fin >= func.now())
    ).
    where(tarifs.is_enabled == 1)
    .correlate(Product)
    .scalar_subquery()
    )

    
    #stocks_subquery
    stocks_subquery = (
       select(
        func.json_arrayagg(
            func.json_object(
                "id", Stock.id,
                "available_stock", Stock.stock_dispo,
                "physical_stock", Stock.stock_physique,
                "is_main", Stock.is_main,
                "warehouse",
                func.if_(
                    (Stock.id_depot == 0) | (Depot.id == None),
                    func.json_object(),
                    func.json_object(
                        "id", Depot.id,
                        "name", Depot.nom
                    )
                )
            )
        )
    )
    .select_from(Stock)
    .outerjoin(Depot, Stock.id_depot == Depot.id)
    .where(Stock.id_produit == Product.id)
    .correlate(Product)
    .scalar_subquery()
    )
    
    #piece_characteristics_subquery
    piece_characteristics_subquery = (
    select(
        func.json_arrayagg(
            func.json_object(
                #id
                "id", characteristic_piece_value.characteristic_id,
                #context
                "context", "piece",
                #value
                "value",
                case((characteristic.type == "boolean",characteristic_piece_value.boolean_value),
                    (characteristic.type == "enum",t_enum.fr),
                    else_=None
                ),
                #value_tr
                "value_tr",
                case(
                    (characteristic.type == "enum",cast(func.json_object(*Translate.json_args(t_enum)), String)),
                    else_=None
                ),
                #min_value
                "min_value",
                case(
                    (
                        characteristic.type == "unit",
                        characteristic_piece_value.min_value
                    ),
                    else_=None
                ),
                #max_value
                "max_value",
                case(
                    (
                        characteristic.type == "unit",
                        characteristic_piece_value.max_value
                    ),
                    else_=None
                ),

                # ENVIRONMENT
                "environment", Environment.label,

                # IS EXCLUSION
                "is_exclusion", characteristic_piece_value.environment_exclusion,
            )
        )
    )
    .select_from(characteristic_piece_value)
    .join(
        characteristic,
        characteristic.id == characteristic_piece_value.characteristic_id
    )
    .outerjoin(
        characteristic_enum,
        characteristic_enum.id == characteristic_piece_value.enum_value_id
    )
    .outerjoin(
        t_enum,
        t_enum.id == characteristic_enum.value
    )
    .outerjoin(
        Environment,
        Environment.id == characteristic_piece_value.environment_id
    )
    .where(characteristic_piece_value.piece_id == Product.id)
    .correlate(Product)
    .scalar_subquery()
    )

    #suppliers_subquery
    suppliers_subquery = (
        select(
            func.json_arrayagg(
                func.json_object(
                    "id", suppliers.id,
                    "supplier_id", suppliers.id_fournisseur,
                    "product_id", suppliers.id_piece,
                    "supplier_reference", suppliers.ref_usine,
                    "buying_price_usd", suppliers.prix_achat,
                    "exchange_rate", suppliers.taux_change,
                    "currency_id", suppliers.id_devise,
                    "buying_price", suppliers.prix_origine,
                    "update_date", suppliers.date
                )
            )
        )
        .select_from(suppliers)
        .where(suppliers.id_piece == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    #machine_characteristics_subquery
    machine_characteristics_subquery = (
    select(
        func.json_arrayagg(
            func.json_object(
                "id", CharacteristicMachine.id_caracteristique,
                "context", "machine",

                #VALUE
                "value",
                func.if_(
                    (UnitsTypes.is_boolean == True) |
                    (UnitsTypes.is_text == True) |
                    (UnitsTypes.is_enum == True),
                    CharacteristicMachine.value,
                    None
                ),

                # MIN
                "min_value",
                func.if_(
                    (UnitsTypes.is_boolean == False) &
                    (UnitsTypes.is_text == False) &
                    (UnitsTypes.is_enum == False),
                    CharacteristicMachine.value,
                    None
                ),

                #MAX
                "max_value",
                func.if_(
                    (UnitsTypes.is_boolean == False) &
                    (UnitsTypes.is_text == False) &
                    (UnitsTypes.is_enum == False),
                    CharacteristicMachine.value,
                    None
                ),

                "environment", func.coalesce(Environment.label, ""),
                "is_exclusion", CharacteristicMachine.environment_exclusion,
             )
           )
        )
    .select_from(CharacteristicMachine)
    .outerjoin(caracteristiques,
        caracteristiques.id == CharacteristicMachine.id_caracteristique
    )
    .outerjoin(units,
        units.id == caracteristiques.id_unit
    )
    .outerjoin(UnitsTypes,
        UnitsTypes.id == units.id_type
    )
    .outerjoin(Environment,
        Environment.id == CharacteristicMachine.environment_id
    )
    .where(CharacteristicMachine.id_produit == Product.id)
    .correlate(Product)
    .scalar_subquery()
    )


    # Resupplies subquery
    resupplies_subquery = (
    select(func.coalesce(func.sum(ot_links.qte), 0))
    .select_from(ot_links)
    .join(ot_colis, ot_links.id_colis == ot_colis.id)
    .join(ot_commandes, ot_commandes.id == ot_colis.id_commande)
    .join(Depot, (Depot.id == ot_colis.id_depot) & (Depot.id_societe == 1))
    .where(
        (ot_links.id_piece == Product.id) &
        (ot_colis.is_shipping == False) &
        (ot_commandes.is_removed == False)
    )
    .correlate(Product)
    .scalar_subquery()
    )

    # Main stock subquery
    main_stock_subquery = (
    select(func.coalesce(func.sum(Stock.stock_dispo), 0))
    .where(
        (Stock.id_produit == Product.id) &
        (Stock.is_main == True)
    )
    .correlate(Product)
    .scalar_subquery()
    )

    # In Stock Logic
    in_stock_expr = case(
    (
        (Product.is_obsolete == 0) &
        (ProductPiece.forcedSale > 0),
        True
    ),
    (main_stock_subquery > 0, True),
    (resupplies_subquery > 0, True),
    else_=False,
    )

    # Resupplies detailed subquery (for product collection)
    resupplies_details_subquery = (
    select(
        func.coalesce(
            func.json_arrayagg(
                func.json_object(
                    "piece_order_id", ot_commandes.id,
                    "warehouse_id", ot_colis.id_depot,
                    "qty", ot_links.qte
                )
            ),
            func.json_array()
        )
    )
    .select_from(ot_links)
    .join(ot_colis, ot_links.id_colis == ot_colis.id)
    .join(ot_commandes, ot_commandes.id == ot_colis.id_commande)
    .join(
        Depot,
        (Depot.id == ot_colis.id_depot) &
        (Depot.id_societe == 1)
    )
    .where(
        (ot_links.id_piece == Product.id) &
        (ot_colis.is_shipping == False) &
        (ot_commandes.is_removed == False)
    )
    .correlate(Product)
    .scalar_subquery()
    )


    # Images subquery
    images_subquery = (
        select(
            func.coalesce(
                func.json_arrayagg(
                    func.json_object(
                        "id", Images.id,
                        "language_id", Images.id_langue,
                        "title", Images.titre,
                        "file", Images.img,
                        "type", Images.type, 
                        "environment", Environment.label,             
                    )
                ),
                func.json_array()
            )
        )
        .select_from(Images)
        .outerjoin(Environment, Images.environment_id == Environment.id)
        .where(Images.id_produit == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    # Accessories subquery
    accessories_subquery = (
        select(
            func.coalesce(
                func.json_arrayagg(Accessories.id_accessoire),
                func.json_array()
            )
        )
        .where(Accessories.id_machine == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    # Alternatives subquery
    alternatives_subquery = (
        select(
            func.coalesce(
                func.json_arrayagg(Alternatives.id_compatible),
                func.json_array()
            )
        )
        .where(Alternatives.id_produit == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    # Videos subquery
    videos_subquery = (
        select(
            func.coalesce(
                func.json_arrayagg(
                    func.json_object(
                        "id", Videos.id,
                        "title", cast(func.json_object(*Translate.json_args(t_video_title)), String),
                        "url", Videos.url,
                        "order", Videos.order,
                        "environment", Environment.label
                    )
                ),
                func.json_array()
            )
        )
        .select_from(Videos)
        .outerjoin(Environment, Videos.environment_id == Environment.id)
        .outerjoin(t_video_title, Videos.title == t_video_title.id)
        .where(
            (Videos.targetId == Product.id) & 
            (Videos.targetTable == 'produits')
        )
        .correlate(Product)
        .scalar_subquery()
    )

    # Aliases subquery
    aliases_subquery = (
        select(
            func.coalesce(
                func.json_arrayagg(
                    func.json_object(
                        "alias", Alias.alias,
                        "category", AliasCategories.nom
                    )
                ),
                func.json_array()
            )
        )
        .select_from(Alias)
        .outerjoin(AliasCategories, Alias.id_categorie == AliasCategories.id)
        .where(Alias.id_produit == Product.id)
        .correlate(Product)
        .scalar_subquery()
    )

    # query

    stmt = select(
        Product.id,
        Product.id_machine,
        Product.id_piece,
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

        # Original Product ID
        Product.id_produit_origine.label('original_product_id'),

        #brand
        Product.id_marque.label('brand'),
        
        # Translation: generated_meta_title -> meta_title
        cast(func.json_object(*Translate.json_args(t_meta_title)), String).label('meta_title'),
        
        # Translation: generated_meta_description -> meta_description
        cast(func.json_object(*Translate.json_args(t_meta_desc)), String).label('meta_description'),
        
        # Translation: generated_original_references -> original_references
        cast(func.json_object(*Translate.json_args(t_orig_refs)), String).label('original_references'),
        
        # Url 
        Product.swapUrl.label('url'),

        #d3e
        func.if_(
            Product.id_d3e != 0,
            cast(
                func.json_object(
                    "id", d3e_direct.id,
                    "company_id", d3e_direct.id_societe,
                    "name", d3e_direct.nom,
                    "price", d3e_direct.prix
                ), String
            ),
            cast(
                func.json_object(
                    "id", d3e_fallback.id,
                    "company_id", d3e_fallback.id_societe,
                    "name", d3e_fallback.nom,
                    "price", d3e_fallback.prix
                ), String
            )
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
        ), String).label("machine"),

       #Piece
       cast(
        func.json_object(
        "id", ProductPiece.id,
        "swap_price", ProductPiece.prix_swap,
        "has_fixed_price", ProductPiece.isLocked,
        "is_consumable", ProductPiece.is_consommable,
        "is_highlighted", ProductPiece.is_alaune,
        "forced_sale_duration", ProductPiece.forcedSale,
        "has_forced_price", ProductPiece.isForced,
        "is_origin", ProductPiece.is_origine,
        "technical_branch", ProductPiece.id_branche_technique
        ),String).label("piece"),


        # Categories
        cast(categories_subquery, String).label("categories"),

        # EXTENSIONS
        extensions_subquery.label("extensions"),

        # Machines and Pieces
        cast(pieces_from_machine_subquery, String).label("pieces"),
        cast(machines_from_piece_subquery, String).label("machines"),
        cast(parts_from_piece_subquery, String).label("parts"),

        # Packaging
        cast(
            func.json_object(
                "product_length", Packaging.produit_x,
                "product_height", Packaging.produit_y,
                "product_depth", Packaging.produit_z,
                "package_length", Packaging.colis_x,
                "package_height", Packaging.colis_y,
                "package_depth", Packaging.colis_z
            ), String
        ).label("packaging"),

        #Documents
        cast(documents_subquery, String).label("documents"),
        
        # Environment
        cast(environment_subquery, String).label("environment"),

        # Pricing
        cast(pricing_subquery, String).label("pricing"),

        # Stocks
        cast(stocks_subquery, String).label("stocks"),

        #Machine characteristics
        cast(machine_characteristics_subquery, String).label("machine_characteristic"),

        #Piece characteristics
        cast(piece_characteristics_subquery, String).label("piece_characteristics"),

        #suppliers
        cast(suppliers_subquery, String).label("suppliers"),


        # in_stock
        in_stock_expr.label("in_stock"),

        # Resupplies detailed
        cast(resupplies_details_subquery, String).label("resupplies"),

        # Images
        cast(images_subquery, String).label("images"),

        # Accessories
        cast(accessories_subquery, String).label("accessories"),

        # Alternatives
        cast(alternatives_subquery, String).label("alternatives"),

        # Videos
        cast(videos_subquery, String).label("videos"),

        # Aliases
        cast(aliases_subquery, String).label("aliases"),



    ).select_from(Product)

    # Joins
    stmt = stmt.outerjoin(t_name, Product.tr_nom == t_name.id)
    stmt = stmt.outerjoin(t_short_desc, Product.generated_short_description == t_short_desc.id)
    stmt = stmt.outerjoin(t_long_desc, Product.generated_long_description == t_long_desc.id)
    stmt = stmt.outerjoin(t_meta_title, Product.generated_meta_title == t_meta_title.id)
    stmt = stmt.outerjoin(t_meta_desc, Product.generated_meta_description == t_meta_desc.id)
    stmt = stmt.outerjoin(t_orig_refs, Product.generated_original_references == t_orig_refs.id)
    
    # D3E Joins
    stmt = stmt.outerjoin(d3e_direct, Product.id_d3e == d3e_direct.id)
    stmt = stmt.outerjoin(ProductMachine, Product.id_machine == ProductMachine.id)
    stmt = stmt.outerjoin(universal_fallback, ProductMachine.id_arborescence == universal_fallback.id)
    stmt = stmt.outerjoin(d3e_fallback, universal_fallback.id_d3e == d3e_fallback.id)
    stmt = stmt.outerjoin(ProductPiece, Product.id_piece == ProductPiece.id)
    stmt = stmt.outerjoin(Packaging, Product.id == Packaging.id_produit)
   



    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    return stmt
