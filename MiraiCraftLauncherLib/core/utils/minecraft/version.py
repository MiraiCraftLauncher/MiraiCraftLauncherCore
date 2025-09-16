from MiraiCraftLauncherLib.core.utils.sources.minecraft import get_version_source
from MiraiCraftLauncherLib.core.utils.net.cache import cache_string_multiple
from MiraiCraftLauncherLib.core.utils.system.text.jtoken import get_jtoken

versions = None

async def load_version(force_refresh:bool = False):
    global versions
    if versions and not force_refresh:
        return
    versions = get_jtoken(await cache_string_multiple(get_version_source()))
    
async def get_version_info(id:str):
    if not versions:
        await load_version()
    for version in versions.get("versions"):
        if id == version.get("id"):
            return version
        
async def search(id:str):
    search_list = []
    await load_version()
    for version in versions.get("versions"):
        if id in version.get("id"):
            search_list.append(version)
    return search_list

async def get_version_info_by_release_time(time:str):
    await load_version()
    for version in versions.get("versions"):
        if time == version.get("releaseTime"):
            return version