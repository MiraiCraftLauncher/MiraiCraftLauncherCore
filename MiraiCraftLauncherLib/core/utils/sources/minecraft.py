from MiraiCraftLauncherLib.core.utils.setup import setup

official = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

bmclapi = "https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json"

async def get_version_source():
    # 自动选择（还没做）
    if setup.get("SourcePrefer") == 0:
        return [
            official,
            bmclapi
        ]
    # 仅官方源
    elif setup.get("SourcePrefer") == 1:
        return [official]
    # 仅镜像源
    else:
        return [bmclapi]
    
async def get_file_source(uri:str):
    # 自动选择（还没做）
    if setup.get("SourcePrefer") == 0:
        return [
            uri,
            uri.replace("piston-meta.mojang.com","bmclapi2.bangbang93.com").replace("libraries.minecraft.net","bmclapi2.bangbang93.com/maven")
        ]
    # 仅官方源
    elif setup.get("SourcePrefer") == 1:
        return [official]
    # 仅镜像源
    else:
        return [bmclapi]
    
async def get_java_source():
    pass
    