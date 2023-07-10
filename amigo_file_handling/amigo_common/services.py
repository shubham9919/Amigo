from amigo_common.common_features.schema_validation import SchemaValidation
from amigo_common.common_features.extract_json import ExctractJsonBody
from amigo_error_handling.errors import BadRequestError, UnsupportedMediaTypeError

class AmigoCommonServices:
    def __init__(self):
        print('Starting Up Amigo Common Services.')
    
    def validate_schema(self, data, endpoint):
        try:
            json_schema = SchemaValidation().load_schema(endpoint)
            return SchemaValidation().is_schema_valid(data, json_schema)
        except BadRequestError as e: 
            raise e
    
    def get_json_body(self, formdata):
        try:
            return ExctractJsonBody().extract_json_body(formdata)
        except Exception as e:
            print(e)
            raise e 
    
    def allowed_file(self, filename):
        ALLOWED_EXTENSIONS =  ['txt',  'pdf', 'png', 'jpg', 'jpeg', 'gif']
        try:
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        except Exception as e:
            print(e)
            raise UnsupportedMediaTypeError("File not supported")