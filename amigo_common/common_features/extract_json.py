import json 

class ExctractJsonBody:
    def extract_json_body(self, body_data):
        try:
            formatted_body  = self.format_body(dict(body_data))
            return json.dumps(formatted_body)
        except Exception as e:
            print(e)
            raise e 

    def format_body(self, data):
        try:
            filtered_data = {key: value for key, value in data.items() if value.strip()}
            return dict(filtered_data)
        except Exception as e:
            print(e)
            raise e
        
