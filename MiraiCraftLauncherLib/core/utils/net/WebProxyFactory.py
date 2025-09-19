from urllib.request import getproxies
from urllib.parse import quote
from MiraiCraftLauncherLib.core.utils.runtime import logger

class WebProxyFactory:
    user_proxy = None
    proxy = None
    disable_proxy = False
    @staticmethod
    def update_proxy():
        if WebProxyFactory.user_proxy:
            WebProxyFactory.proxy = WebProxyFactory.user_proxy
        _proxy = getproxies()
        http = _proxy.get("http")
        https = _proxy.get("https")
        if http:
            _proxy["http://"] = http
        if https:
            _proxy["https://"] = https
        if _proxy and WebProxyFactory.proxy != _proxy:
            WebProxyFactory.proxy = _proxy
            return True
        logger.debug("Network",f"当前系统代理为 {WebProxyFactory.proxy}")
        return False
    @staticmethod
    def setup_user_proxy(proxy_addr:str,proxy_port:int,proxy_user:str,proxy_password:str):
        proxy_auth = ""
        if proxy_user:
            proxy_auth += proxy_user
        if proxy_password:
            proxy_auth += f":{proxy_password}" if proxy_user else proxy_password
        if proxy_addr.startswith("sock"):
            raise ValueError("Unsupport sock5 proxy.")
        protocol = proxy_addr.split("://",1)[0]
        proxy_addr = f"{protocol}://{quote(proxy_auth)}@{proxy_addr}:{proxy_port}"
        WebProxyFactory.user_proxy = {
            "http://": proxy_addr,
            "https": proxy_addr,
        }
        return WebProxyFactory.user_proxy
    @staticmethod
    def reset_proxy():
        WebProxyFactory.user_proxy = None