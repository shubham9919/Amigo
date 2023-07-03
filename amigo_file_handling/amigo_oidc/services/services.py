from amigo_oidc.identity_providers.google_oidc.services import GoogleOIDC

class OIDC: 
    def __init__(self, identity_provider=None):
        print('starting the oidc impl for amigo')
        self.identity_provider = None
        if identity_provider == 'google':
            # trigger google oidc flow 
            print('initiating google oidc flow.')
            self.identity_provider = identity_provider
            
        elif identity_provider is None: 
            print('identity provider not provided.')
    
    def initiate_oidc(self):
        if self.identity_provider == "google":
            return GoogleOIDC().auth_google()

