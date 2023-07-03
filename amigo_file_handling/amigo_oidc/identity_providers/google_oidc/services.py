
import requests
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, flash, request, redirect, url_for
import json


class GoogleOIDC:
    def __init__(self):
        self.GOOGLE_CLIENT_ID = "====="
        self.GOOGLE_CLIENT_SECRET = "=========="
        self.GOOGLE_DISCOVERY_URL = (
            "https://accounts.google.com/.well-known/openid-configuration"
        )
        self.DISCOVERY_RESPONSE = None
        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)

    def get_google_provider_config(self):
        self.DISCOVERY_RESPONSE = requests.get(self.GOOGLE_DISCOVERY_URL).json()
        return self.DISCOVERY_RESPONSE

    def auth_google(self):
        google_provider_config = self.DISCOVERY_RESPONSE if self.DISCOVERY_RESPONSE is not None else self.get_google_provider_config()
        authorization_endpoint = google_provider_config["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )

        return request_uri
    
    def process_auth_google(self):
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
            return "User email not available or not verified by Google.", 400
        

    
    def get_token(self, token_endpoint):
        # Authorization code Sent by Google IDP 
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