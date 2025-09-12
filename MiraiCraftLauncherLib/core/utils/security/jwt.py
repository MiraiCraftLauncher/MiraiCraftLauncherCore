import jwt

from MiraiCraftLauncherLib.core.utils.system.text.json import get_jtoken
from MiraiCraftLauncherLib.core.utils.net.web import download_string

async def validate_jwt_signature(jtoken:str,openid_condigure_addr:str,client_id:str):
    """验证 JWT 签名，并返回 payload"""
    try:
        configure = get_jtoken(download_string(openid_condigure_addr))
        jwk_url = configure.get("jwks_uri")
        jwt_headers = jwt.get_unverified_header(jtoken)
        algorithm = jwt_headers.get("alg")
        kid = jwt_headers.get("kid")
        jwks = get_jtoken(download_string(jwk_url))
        for key in jwks.items():
            current_kid = key.get("kid")
            if kid == current_kid:
                jwk = jwt.PyJWK(key)
                return jwt.decode(jtoken,jwk.key,algorithm)
    except Exception as e:
        return ""