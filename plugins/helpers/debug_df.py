import json

def debug_df(df):
    # Get first row
    first_row = df.head(1)

    # Convert to dict (scalar values)
    row_dict = {col: values[0] for col, values in first_row.to_dict(as_series=False).items()}

    # Get types
    row_types = {col: str(df.schema[col]) for col in row_dict.keys()}

    # Combine values and types
    row_with_types = {col: {"value": row_dict[col], "type": row_types[col]} for col in row_dict.keys()}
    print(first_row.rows())
    print(json.dumps(row_with_types, indent=2))