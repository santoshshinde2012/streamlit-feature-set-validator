import pandas as pd


def infer_type(value):
    """Infer JSON schema type and constraints from value."""
    if isinstance(value, bool):
        return {"type": "boolean"}
    elif isinstance(value, int):
        return {"type": "integer", "minimum": 0}
    elif isinstance(value, float):
        return {"type": "number"}
    elif isinstance(value, str):
        return {"type": "string", "minLength": 1}
    else:
        return {"type": "string"}


def generate_json_schema(df: pd.DataFrame) -> dict:
    """Generate JSON schema from the first record in the DataFrame."""
    if df is None or df.empty:
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {},
            "required": [],
        }

    first_record = df.iloc[0].to_dict()
    properties = {key: infer_type(value) for key, value in first_record.items()}

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": properties,
        "required": list(properties.keys()),
    }

    return schema
