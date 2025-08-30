import aiohttp
import asyncio
from urllib.request import getproxies

loop = asyncio.get_event_loop()

client = aiohttp.ClientSession(loop=loop)

http_proxy = None

http_err = range(400,600)
async def get_http_transport_proxy():
    if http_proxy:
        return http_proxy
    return getproxies()

async def request(url:str,method:str = "GET",headers:dict[str,str] = {},data=None,timeout:int=25000,retry:int=3):
    response = await client.request(method,url,headers=headers,timeout=timeout,data=data)