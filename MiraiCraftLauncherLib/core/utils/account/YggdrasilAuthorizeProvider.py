from IAuthorizeProvider import IAuthorizeProvider

class YggdrasilAuthorizeProvider(IAuthorizeProvider):
    def __init__(self,username:str,password:str):
        self.username,self.password = username,password
    async def authenticate():
        pass