import jsonschema
from jsonschema import validate

class JSONAgent:
    def __init__(self, schema_path: str):
        self.schema = self._load_schema(schema_path)

    def _load_schema(self, path: str) -> dict:
        import json
        with open(path) as f:
            return json.load(f)

    def validate(self, json_data: dict) -> dict:
       try:
         validate(instance=json_data, schema=self.schema)
         return {"status": "valid", "data": json_data}
       except jsonschema.ValidationError as e:
         return {
            "status": "error",
            "message": e.message,
            "path": list(e.path),
            "validator": e.validator
        }
