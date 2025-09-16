from MiraiCraftLauncherLib.core.utils.net.cache import cache_string
from MiraiCraftLauncherLib.core.utils.net.downloader import NetFile,NetTask
from MiraiCraftLauncherLib.core.utils.system.text.jtoken import get_jtoken
from MiraiCraftLauncherLib.core.utils.sources.minecraft import get_file_source
from MiraiCraftLauncherLib.core.utils.environment import current_minecraft_path,os_name,get_system_arch
from version import get_version_info
import pathlib
import platform

async def install(version:str):
    version_info = get_version_info(version)
    if not version_info:
        raise KeyError("Version not found.")
    
async def get_mc_lib(jtoken:dict,version_name:str,require_mapping:bool = False) -> tuple[list[NetFile],list[NetFile]]:
    """获取支持库列表"""
    native = {}
    stdlib = {}
    client = jtoken.get("downloads").get("client")
    stdlib["net.minecraft.clinet"] = NetFile(get_file_source(client.get("url")),pathlib.Path(current_minecraft_path,"versions",version_name,f"{version_name}.jar"),0,client.get("size"),"sha1",client.get("sha1"))
    if require_mapping:
        mapping = jtoken.get("downloads").get("client_mappings")
        stdlib["net.minecraft.client.client_mapping"] = NetFile(get_file_source(mapping.get("url")),pathlib.Path(current_minecraft_path,"libraries","net","minecraft","client",f"{version_name}.txt"))
    for library in jtoken.get("libraries"):
        artifact = library.get("downloads").get("artifact")
        classifier = library.get("downloads").get("classifiers")
        skip_native = False
        if artifact:
            stdlib.append(
                NetFile(get_file_source(artifact.get("url")),pathlib.Path(current_minecraft_path,"libraries",artifact.get("path")),0,artifact.get("size"),"sha1",artifact.get("sha1"))
                )
        # 需要检查是否可用
        if classifier:
            native_key = library.get("natives").get(os_name)
            rules = library.get("rules")
            for rule in rules.items():
                if rule.get("action") == "disallow":
                    if rule.get("os").get("name") == os_name.lower():
                        skip_native = True
                        break
            if skip_native:
                continue
            if "${arch}" in native_key:
                native_key = native_key.replace("${arch}",get_system_arch())
            native_file = classifier.get(native_key)
            if native_file:
                native.append(NetFile(get_file_source(native_file.get("url")),pathlib.Path(current_minecraft_path,"libraries",native_file.get("path")),0,native_file.get("size"),"sha1",native_file.get("sha1")))
    return native,stdlib

async def get_assets(jtoken:dict):
    assets = jtoken.get("assetsIndex")

async def get_old_argument(jtoken:dict):
    return jtoken.get("minecraftArguments","").split(" ")

async def get_new_argument(jtoken:dict):
    game = jtoken.get("arguments",{}).get("game")
    jvm = jtoken.get("arguments",{}).get("jvm")
    game_arguments = []
    jvm_arguments = []
    for game_arg in game:
        if isinstance(game_arg,str):
            game_arguments.append(game_arg)
        else:
            for rule in game_arg.get("rules"):
                # Game Argument 不区分操作系统或硬件架构，所以不检查是否符合 xx 规则的情况（翻遍了 Json 也没看到有硬件架构或者操作系统）
                # 所以炸了就是 Bugjump 的锅
                if rule.get("action") == "disallow":
                    break
                values = game_arg.get("value")
                if isinstance(values,str):
                    game_arguments.append(values)
                else:
                    game_arguments.extend(values)
                break
    for jvm_arg in jvm:
        # Json 中也有只允许单个操作系统的情况，所以默认值设为 False
        should_add = False
        if isinstance(jvm_arg,str):
            jvm_arguments.append(jvm_arg)
        else:
            for rule in jvm_arg.get("rules"):
                os = rule.get("os")
                system_name = os.get("name")
                arch = os.get("arch")        
                if rule.get("action") == "disallow":
                    if arch:
                        # 架构对不上就没有检查下一个条件的必要了
                        if arch != get_system_arch():
                            continue
                        if (arch and arch == get_system_arch()) and (system_name and system_name == os_name):
                            should_add = False
                            break
                    
                elif rule.get("action") == "allow":
                    if arch:
                        if arch != get_system_arch():
                            continue
                    if system_name:
                        if system_name != os_name:
                            continue
            if should_add:
                values = jvm_arg.get("value")
                if isinstance(values,str):
                    jvm_arguments.append(values)
                else:
                    jvm_arguments.extend(values)

async def deduplicate_argument():
    """对参数进行去重"""
    pass

async def apply_security(arguments:list[str]):
    """
    用于应用安全相关的参数
    """
    pass

async def apply_custom_argument(arguments:list[str]):
    """应用自定义参数"""
    pass

async def apply_authlib_injector():
    """应用 Authlib-Injector"""
    pass

async def apply_argument():
    """对参数内的占位符替换为实际值"""
    pass

async def get_launch_argument():
    pass

async def check_file(files:list[NetFile]):
    pass

async def update_assets_index():
    pass