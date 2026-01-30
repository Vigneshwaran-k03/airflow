from sqlalchemy import select, func, cast, String, case, literal_column
from sqlalchemy.orm import aliased
from models.characteristics_piece import Characteristic, characteristic_piece_value, Unit
from models.translation import Translate

def characteristics_piece_base_query(limit: int = None, offset: int = None):
    # Aliases
    t_name = aliased(Translate)
    t_unit_name = aliased(Translate)
    
    # Subquery for product_ids
    products_ids_subquery = (
        select(func.json_arrayagg(characteristic_piece_value.piece_id))
        .where(characteristic_piece_value.characteristic_id == Characteristic.id)
        .correlate(Characteristic)
        .scalar_subquery()
    )

    stmt = (
        select(
            # Primary fields
            Characteristic.id.label("id"),
            Characteristic.technical_branch_id.label("technical_branch_id"),
            Unit.symbol.label("symbol"),
            
            # Type logic: "unit" -> "number"
            case(
                (Characteristic.type == 'unit', 'number'),
                else_=Characteristic.type
            ).label("type"),

            # Array of product IDs
            cast(products_ids_subquery, String).label("products_ids"),

            # Translations (JSON as columns)
            cast(func.json_object(*Translate.json_args(table=t_name)), String).label("name"),
            cast(func.json_object(*Translate.json_args(table=t_unit_name)), String).label("unit"),
        )
        .select_from(Characteristic)
        .outerjoin(t_name, Characteristic.name == t_name.id)
        .outerjoin(Unit, Characteristic.unit_id == Unit.id)
        .outerjoin(t_unit_name, Unit.name == t_unit_name.id)
    )
    
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)
        
    return stmt
