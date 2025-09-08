import aiohttp
import asyncio
from urllib.request import getproxies
import webbrowser
from MiraiCraftLauncherLib.core.utils.internal import *

loop = asyncio.get_event_loop()

client = aiohttp.ClientSession(loop=loop)

http_proxy = None

http_err = range(400,600)
async def get_http_transport_proxy():
    if http_proxy:
        return http_proxy
    return getproxies()

async def request(
        url:str,
        method:str = "GET",
        headers:dict[str,str] = {},
        data=None,
        timeout:int=25000,
        content_type:str = "application/json",
        accept:str = "application/json",
        ) -> aiohttp.ClientResponse:
    secret_sign(url,headers)
    if not (method.upper == "GET" or method.upper() == "HEAD") and data:
        if not headers.get("Content-Type"):
            headers["Content-Type"] = content_type
        if not headers.get("Accept"):
            headers["Accept"] = accept
    return await client.request(method.upper(),url,headers=headers,timeout=timeout,data=data)
    

async def request_retry(
        url:str,
        method:str = "GET",
        headers:dict[str,str] = {},
        data=None,
        timeout:int=25000,
        content_type:str = "application/json",
        accept:str = "application/json",
        authorization:str = None,
        retry:int = 3) -> aiohttp.ClientResponse:
    lastException = None
    for tired in range(retry):
        try:
            return await request(url,method,headers,data,timeout,content_type,accept,authorization)
        except aiohttp.ClientError as e:
            lastException = e
            await asyncio.sleep(tired * 100)
    if lastException:
        raise lastException

async def download_string(url:str,headers:dict[str,str]) -> str:
    return (await request_retry(url,"GET",headers)).text("utf-8")

def secret_sign(url:str,headers:dict[str,str]):
    if "api.curseforge.com" in url:
        headers["x-api-key"] = curseforge_api_key
    if "minecraftforge.net" in url:
        headers["User-Agent"] = f"{launcher_name}/{launcher_version} Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
    headers["User-Agent"] = f"{launcher_name}/{launcher_version}"

def open_in_web_browser(url:str):
    webbrowser.open(url)