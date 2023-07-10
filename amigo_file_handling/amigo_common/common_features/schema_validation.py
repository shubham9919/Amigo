import json
import jsonschema
from amigo_error_handling.errors import BadRequestError, InternalServerError

class SchemaValidation:

    def load_schema(self, endpoint):
        try:
            if endpoint == 'user/login':
                schema_file_path = 'schema/user_login.json'
            elif endpoint == 'user/info':
                schema_file_path = 'schema/user_info.json'
            with open(schema_file_path, 'r') as schema_file:
                # Load the contents of the schema file as a JSON object
                schema = json.load(schema_file)
            return json.dumps(schema)
        except Exception as e: 
            print("Error: ", e)
            raise InternalServerError("Error While loading schema.")

    def is_schema_valid(self, json_body, schema):
        try:
            print(json.loads(json_body))
            jsonschema.validate(json.loads(json_body), json.loads(schema))
            print("Validation successful!")
            return True
        except jsonschema.ValidationError as e:
            print("Validation failed. Errors:")
            print(e)
            raise BadRequestError(e)