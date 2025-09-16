from enum import Enum
from MiraiCraftLauncherLib.core.utils.net.web import request_retry
from MiraiCraftLauncherLib.core.models.exceptions.AuthenticationException import *
from MiraiCraftLauncherLib.core.utils.net.web import download_string
from MiraiCraftLauncherLib.core.utils.security import hash
from MiraiCraftLauncherLib.core.utils.system.text.jtoken import get_jtoken
from MiraiCraftLauncherLib.core.utils.system.text.secret import get_encrypt_safe_random_int
from urllib import parse
import secrets
import base64
import msal

class LoginType(Enum):
    Device = 1
    Authorize = 2
    WAM = 3

class ErrorType(Enum):
    AccessDenied = 0
    ServerError = 1
    InternalError = 2


class SimpleOAuthClient:
    def __init__(self,client_id:str,token_endpoint:str,device_endpoint:str = None,authorize_endpoint:str = None,is_ms_entra_id:bool = True):
        self._oauth20_result_list = {}
        self.token_endpoint = token_endpoint
        self.device_endpoint = device_endpoint
        self.authorize_endpoint = authorize_endpoint
        if not client_id:
            raise ValueError("Invalid parameter: cliend_id")
        self._client = client_id
        self._login_request_list = {}
        if is_ms_entra_id:
            self._msal_client = msal.PublicClientApplication(client_id,authority="https://login.microsoftonline.com/consumers")
    async def authorize(self):
        if not self.authorize_endpoint:
            raise AuthenticationException("Invalid parameter: authorize_endpoint is invalid")
    async def device():
        pass
    async def authorize_msentra_id():
        pass
    async def device_msentra_id():
        pass
    
    async def build_login_info(self,scope:list[str],token_endpoint:str,refresh:str = None,redirect_uri:str = None,authorize_uri:str = None,openid_config_uri:str = None,login_type:LoginType = LoginType.Authorize,use_msal:bool = True) -> dict:
        query = {
            "client_id": self._client,
            "scope": " ".join(scope)
        }
        state = get_encrypt_safe_random_int(15)
        if not authorize_uri:
            if not openid_config_uri:
                raise ValueError("Invalid parameter: openid_config_uri")
            config = get_jtoken(download_string(openid_config_uri))
        authorize_uri = config.get("device_authorization_endpoint") if login_type == LoginType.Device else None
        
        if login_type == LoginType.Authorize:
            if self._msal_client and use_msal:
                self._login_request_list[state] =  self._msal_client.initiate_auth_code_flow()
                self._login_request_list[state]["is_msal"] = True
                self._login_request_list[state]["type"] = LoginType.Authorize
                return {
                    "code": None,
                    "verification_uri": None,
                    "verification_uri_complete": None
                }
        
            if not authorize_uri:
                raise ValueError("Invalid parameter: authorize_uri")
            exchange_verifier = secrets.token_urlsafe(96)
            base64_url = base64.urlsafe_b64encode(exchange_verifier.encode()).decode().removesuffix("=")
            pkce = hash.sha256(data=base64_url)
            query["response_type"] = "code"
            query["redirect_uri"] = redirect_uri
            query["state"] = state
            query["code_challenge"] = pkce
            query["code_challenge_method"] = "S256"
            login_url = f"{authorize_uri}?{parse.urlencode(query)}"
            self._login_request_list[state] = {
                "type": LoginType.Authorize
            }
            return {
                "code": None,
                "verification_uri": None,
                "verification_uri_complete": login_url
            }
        
        elif login_type == LoginType.Device:
            if self._msal_client and use_msal:
                self._login_request_list[state] = flow = self._msal_client.initiate_device_flow()
                
                return {
                    "code": flow.get("user_code"),
                    "verification_uri": flow.get("verification_uri"),
                    "verification_uri_complete": None
                }
            data = parse.urlencode(query)
            response = await request_retry(authorize_uri,"POST",data=data,content_type="application/x-www-form-urlencoded")
            response.raise_for_status()
            response_json = get_jtoken(response.text("utf-8"))
            self._login_request_list[state] = {
                "device_code": response_json.get("device_code"),
                "interval": response_json.get("interval")
            }
            return {
                "code": response_json.get("user_code"),
                "verification_uri": response_json.get("verifcation_uri"),
                "verification_uri_complete": response_json.get("verifcation_uri_complete")
            }

    async def get_user_authorize_info(self,id:int):
        result = self._login_request_list[id]
        if result.get("type") == LoginType.Authorize:
            if result.get("is_msal"):
                self._msal_client.acquire_token_by_auth_code_flow(result)   
        else:
            if result.get("is_msal"):
                self._msal_client.acquire_token_by_device_flow(result)
            response = await request_retry()
    async def _oauth20_callback():
        pass
    async def refresh():
        pass