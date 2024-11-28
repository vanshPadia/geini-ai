from app.llm.schemas.refinement_schema import FlightRefinement
from pydantic import BaseModel


def get_filtered_schema(model: BaseModel):
    schema = model.model_json_schema()
    filtered_schema = {}

    for field, details in schema.get("properties", {}).items():
        field_type = details.get("type")  # Direct type if available

        # Handle 'anyOf' and exclude 'null' (Optional)
        if not field_type and "anyOf" in details:
            field_type = ", ".join(
                sub_type.get("type", "unknown")
                for sub_type in details["anyOf"]
                if sub_type.get("type") != "null"  # Exclude null
            )

        filtered_schema[field] = {
            "type": field_type,  # The actual type without 'Optional'
            "default": details.get("default"),
            "description": details.get("description")
        }

    return filtered_schema


def populate_null_fields(target: FlightRefinement, source: FlightRefinement) -> FlightRefinement:
    if target and source:
        for field_name, target_value in target.model_dump().items():
            # Check if the field in target is None and the corresponding field in source has a value
            if target_value is None:
                source_value = getattr(source, field_name, None)
                if source_value is not None:
                    setattr(target, field_name, source_value)