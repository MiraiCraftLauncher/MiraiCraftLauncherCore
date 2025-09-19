from httpx import AsyncClient,Response,ConnectError
from urllib.request import Request,getproxies,urlopen
from urllib.parse import quote
from WebProxyFactory import WebProxyFactory
from MiraiCraftLauncherLib.core.utils.environment import context,cache_responses,data_handle_obj
from MiraiCraftLauncherLib.core.utils.internal import curseforge_api_key,launcher_name,launcher_version
from MiraiCraftLauncherLib.core.utils.runtime import logger
import pathlib
import asyncio


client = AsyncClient(http2=True,proxy=WebProxyFactory.proxy,verify=context)

class WebResponse:
    def __init__(self,status_code:int,headers:dict[str,str],inner_response):
        self.status_code = status_code
        self.headers = headers
        self.inner_response = inner_response
    async def read():
        pass

class WebRequestFactory:
    def __init__(self):
        pass
    @staticmethod
    async def request(request_message:Request):
        global client
        if WebProxyFactory.update_proxy():
            await client.aclose()
            client = AsyncClient(http2=True,proxy=WebProxyFactory.proxy,verify=context)
        cached_response = WebRequestFactory.on_request_start(request_message)
        if not request_message.full_url.startswith("http"):
            raise ValueError("Url must starts with http or https.")
        response = await client.request(
            request_message.method.upper(),
            request_message.full_url,
            headers=request_message.headers,
            data=request_message.data,timeout=request_message.timeout)
        if WebRequestFactory.on_request_end(response):
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
        response = cache_responses.get(request.full_url)
        if response:
            etag = response.get("ETag")
            request.add_header("If-None-Matched",etag)
        return WebResponse(200,{"X-Response-Source":"Internal Cache Response"},"9")
    @staticmethod
    def on_request_end(response:Response):
        # 缓存处理
        if response.status_code == 304:
            return True
        cache_response = cache_responses.get(response.request.url)
        if not response:
            return False
        if not cache_response:
            return False
        pathlib.Path(cache_response.get("path")).unlink(True)
        del cache_response[response.request.url]
        if response.is_success:
            cache_response[response.request.url] = {
                "path":"",
                "ETag": response.headers.get("ETag")
            }
    @staticmethod
    async def request_retry(request_message:Request,retry:int = 3,retry_policy = lambda retry: retry * 100,make_log:bool = True):
        for tried in range(retry + 1):
            try:
                logger.debug("Network",f"发送网络请求（{request_message.full_url}），最大超时 {request_message.timeout} ms")
                return await WebRequestFactory.request(request_message)
            except ConnectError as ex:
                
                logger.error("Network",f"发送可重试的网络请求失败")
            except Exception:
                logger.error("Network",f"发送可重试的网络请求失败")
                pass

request = Request(url="https://hmcl.net",method="GET")
request.timeout = 25000

r = asyncio.run(WebRequestFactory.request_retry(request))

print(r.inner_response.http_version)

#print(r.inner_response.text)