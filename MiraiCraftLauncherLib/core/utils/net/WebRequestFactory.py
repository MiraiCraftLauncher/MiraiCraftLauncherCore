from httpx import AsyncClient,Response
from urllib.request import Request,getproxies,urlopen
from urllib.parse import quote
from WebProxyFactory import WebProxyFactory
from MiraiCraftLauncherLib.core.utils.environment import context,cache_response,data_handle_obj
from MiraiCraftLauncherLib.core.utils.internal import curseforge_api_key,launcher_name,launcher_version
import pathlib

client = AsyncClient(http2=True,proxy=WebProxyFactory.proxy,verify=context)

class WebResponse:
    def __init__(self,status_code:int,headers:dict[str,str],inner_response):
        self.status_code = status_code
        self.headers = headers
        self.inner_response = inner_response

class WebRequestFactory:
    def __init__(self):
        pass
    @staticmethod
    def request_other():
        return 
    @staticmethod
    async def request(request_message:Request):
        global client
        if WebProxyFactory.update_proxy():
            await client.aclose()
            client = AsyncClient(http2=True,proxy=WebProxyFactory.proxy)
        cached_response = WebRequestFactory.on_request_start(request_message)
        if not request_message.full_url.startswith("http"):
            raise ValueError("Url must starts with http or https. Use request_other to send request with other protocol")
        response = await client.request(
            request_message.method.upper(),
            request_message.full_url,
            headers=request_message.headers,
            data=request_message.data,timeout=request_message.timeout)
        if await WebRequestFactory.on_request_end(response):
            return cached_response
        return WebResponse(response.status_code,response.headers,response)
    @staticmethod
    def on_request_start(request:Request):
        # 添加鉴权信息
        if "api.curseforge.com/" in request.full_url:
            request.add_header("x-api-key",curseforge_api_key)
        if "minecraftforge.net" in request.full_url:
            request.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")  
        if not request.headers.get("User-Agent"):
            request.add_header("User-Agent",f"{launcher_name}/{launcher_version}")
        # 暂时不对非 GET 进行响应缓存
        if request.method != "GET":
            return None
        # 减轻服务器响应压力
        response = cache_response.get(request.full_url)
        if response:
            etag = response.get("ETag")
            request.add_header("If-None-Matched",etag)
        return WebResponse(200,{"X-Response-Source":"Internal Cache Response"})
    @staticmethod
    def on_request_end(response:Response):
        # 缓存处理
        if response.status_code == 304:
            return True
        cache_response = cache_response.get(response.request.url)
        if not response:
            return False
        pathlib.Path(cache_response.get("path")).unlink(True)
        del cache_response[response.request.url]
        if response.is_success:
            cache_response[response.request.url] = {
                "path":"",
                "ETag": r
            }