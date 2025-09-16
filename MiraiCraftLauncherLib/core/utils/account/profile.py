from IAuthorizeProvider import IAuthorizeProvider

class Profile:
    def __init__(self,provider:IAuthorizeProvider,access_token:str,player_name:str,skin_url:str,refresh_token:str = None,cape_url:str = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.player_name = player_name
        self.skin_url = skin_url
        self.cape_url = cape_url
