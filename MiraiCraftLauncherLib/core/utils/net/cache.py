import gzip
import pathlib
import json
from web import request_retry
from MiraiCraftLauncherLib.core.utils.environment import app_data

cache_database_path = pathlib.Path(app_data,"/cache/etag/data.json")

cachedata:dict[str,dict[str,str]] = None

with cache_database_path.open("r") as f:
    cachedata = json.load(f)

async def cache_string(url:str,headers:dict[str,str],except_hash:str = "",timeout:int = 25000):
    file = cachedata.get(url)
    if file:
        headers["If-None-Match"] = file.get("etag")
    response = await request_retry(url,"GET",headers)
    if response.status != 304:
        text = response.text("utf-8")
        gzip_stream = gzip.GzipFile()
        with pathlib.Path(app_data,f"/cache/files/{except_hash}").open("w") as f:
            f.write(text)
        
        return text
    return 
