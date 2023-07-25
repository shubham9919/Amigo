
import requests
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, flash, request, redirect, url_for
from amigo_error_handling.errors import ServiceUnavailableError, BadRequestError
import json
    

class GoogleOIDC:
    def __init__(self):
        self.GOOGLE_CLIENT_ID = "1003011779946-ldergf50m2a2t49cvuf8tige2t0qmie6.apps.googleusercontent.com"
        self.GOOGLE_CLIENT_SECRET = "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"
        self.GOOGLE_DISCOVERY_URL = (
            "https://accounts.google.com/.well-known/openid-configuration"
        )
        self.DISCOVERY_RESPONSE = None
        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)

    def get_google_provider_config(self):
        try:
            self.DISCOVERY_RESPONSE = requests.get(self.GOOGLE_DISCOVERY_URL).json()
            return self.DISCOVERY_RESPONSE
        except Exception as e:
            print("Error: ",e)
            raise ServiceUnavailableError("google openid configuration api not available.")

    def auth_google(self):
        try:
            google_provider_config = self.DISCOVERY_RESPONSE if self.DISCOVERY_RESPONSE is not None else self.get_google_provider_config()
            authorization_endpoint = google_provider_config["authorization_endpoint"]
            request_uri = self.client.prepare_request_uri(
                authorization_endpoint,
                redirect_uri=request.base_url + "/callback",
                scope=["openid", "email", "profile"],
            )
            return request_uri
        except ServiceUnavailableError as e: 
            raise e 
        except Exception as e: 
            print("Error: ", e)

    
    def process_auth_google(self):
        try:
            google_provider_config = self.DISCOVERY_RESPONSE if self.DISCOVERY_RESPONSE is not None else self.get_google_provider_config()
            token_endpoint = google_provider_config["token_endpoint"]
            get_token_res = self.get_token(token_endpoint)
            # Mask the token in production.
            print('Token found to initiate OIDC with Google IDP server.', get_token_res)
            userinfo_endpoint = google_provider_config["userinfo_endpoint"]
            uri, headers, body = self.client.add_token(userinfo_endpoint)
            userinfo_response = requests.get(uri, headers=headers, data=body)
            if userinfo_response.json().get("email_verified"):
                return userinfo_response.json()
            else:
                raise BadRequestError("User email not available or not verified by Google.")
        except ServiceUnavailableError as e: 
            raise e 
        except Exception as e:
            print(e)
            raise e 

        

    
    def get_token(self, token_endpoint):
        # Authorization code Sent by Google IDP 
        try:
            code = request.args.get("code")
            token_url, headers, body = self.client.prepare_token_request(
                token_endpoint,
                authorization_response=request.url,
                redirect_url=request.base_url,
                code=code
            )
            token_response = requests.post(
                token_url,
                headers=headers,
                data=body,
                auth=(self.GOOGLE_CLIENT_ID, self.GOOGLE_CLIENT_SECRET),
            )
            return self.client.parse_request_body_response(json.dumps(token_response.json()))
        except Exception as e: 
            print("Error: ", e)