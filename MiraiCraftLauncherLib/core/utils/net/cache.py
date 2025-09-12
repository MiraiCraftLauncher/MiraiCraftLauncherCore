import gzip
import pathlib
import json
from web import download_string,request_retry,request_with_multiple_source
from MiraiCraftLauncherLib.core.utils.environment import app_data

cache_database_path = pathlib.Path(app_data,"/cache/etag/data.json")

cachedata:dict[str,dict[str,str]] = None

with cache_database_path.open("r") as f:
    cachedata = json.load(f)

async def cache_request_multiple(
        urls:list[str],
        method:str = "GET",
        headers:dict[str,str] = {},
        data=None,
        timeout:int=25000,
        content_type:str = "application/json",
        accept:str = "application/json",
):
    """支持缓存和多来源的网络请求"""
    return await request_with_multiple_source(urls,method,headers,data,timeout,content_type,accept)

async def cache_string_multiple(urls:list[str],headers:dict[str,str] = None,except_hash:str = "",hash_provider = None,timeout:int = 25000):
    return await cache_request_multiple(urls,headers = headers,timeout=timeout)
    

async def cache_request(url:str,method:str = "GET",headers:dict[str,str] = {},data = None,timeout:int = 25000):
    return await request_retry(url,method,headers,data,timeout)

async def cache_string(url:str,headers:dict[str,str] = None,except_hash:str = "",hash_provider = None,timeout:int = 25000):
    data = download_string(url,headers)
    if except_hash or hash_provider(data) == except_hash:
        return data
    raise ValueError("Invalid Hash")
    file = cachedata.get(url)
    if file:
        headers["If-None-Match"] = file.get("etag")
    response = await request_retry(url,"GET",headers)
    if response.status != 304:
        text = response.text("utf-8")
        with pathlib.Path(app_data,f"/cache/files/{except_hash}").open("w") as f:
            f.write(text)
        
        return text
    return 
