from sqlalchemy import select, func, cast, String, case
from sqlalchemy.orm import aliased
from models.characteristics_machine import CharacteristicMachine, CharacteristicProduct, Unit, UnitType
from models.translation import Translate
from models.products import Product

def characteristics_machine_base_query(limit: int = None, offset: int = None):
    # Aliases for translation tables
    t_name = aliased(Translate)
    t_unit_name = aliased(Translate)
    
    # Subquery for product_ids
    products_ids_subquery = (
        select(func.json_arrayagg(CharacteristicProduct.id_produit))
        .join(Product, CharacteristicProduct.id_produit == Product.id)
        .where(CharacteristicProduct.id_caracteristique == CharacteristicMachine.id)
        .correlate(CharacteristicMachine)
        .scalar_subquery()
    )

    stmt = (
        select(
            # Primary fields
            CharacteristicMachine.id.label("id"),
            
            # Type logic based on units_type conditions
            case(
                (UnitType.is_text == True, 'Enum'),
                (UnitType.is_enum == True, 'Enum'),
                (UnitType.is_boolean == True, 'boolean'),
                else_='number'
            ).label("type"),
            
            # Unit symbol
            Unit.unit.label("symbol"),
            
            # Array of product IDs
            cast(products_ids_subquery, String).label("product_ids"),
            
            # Translations (JSON as columns)
            cast(func.json_object(*Translate.json_args(table=t_name)), String).label("name"),
            cast(func.json_object(*Translate.json_args(table=t_unit_name)), String).label("unit"),
        )
        .select_from(CharacteristicMachine)
        .outerjoin(t_name, CharacteristicMachine.tr_nom == t_name.id)
        .outerjoin(Unit, CharacteristicMachine.id_unit == Unit.id)
        .outerjoin(t_unit_name, Unit.tr_nom == t_unit_name.id)
        .outerjoin(UnitType, Unit.id_type == UnitType.id)
    )
    
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)
        
    return stmt
