import certifi
import ssl
import stat
import platform
import os
import pathlib
import getpass
import sys
from MiraiCraftLauncherLib.core.utils.system.os.info import system_type,SystemType
from enum import Enum
from MiraiCraftLauncherLib.core.utils.system.text.jtoken import get_jtoken

class ConfigProvider(Enum):
    File = 0
    Registry = 1

app_debug = True

executable_path = pathlib.Path(sys.executable).parent

app_data = f"{executable_path}/data/{getpass.getuser()}" if SystemType.Windows == system_type else f"/etc/MiraiCL/{getpass.getuser()}/data"

print(system_type)

minecraft_folder = os.getenv("appdata") if system_type == SystemType.Windows else pathlib.Path.home().joinpath(".minecraft")

easy_tier_path = f"{app_data}/link/core/easytier"

secret_path = pathlib.Path(f"{app_data}/secret")

if not secret_path.exists():
    secret_path.mkdir(600,True,True)

if stat.S_IMODE(secret_path.stat().st_mode) != 600:
    secret_path.chmod(600)

current_minecraft_path = ""

os_name = platform.system()

arch = platform.machine()
    
authlib_injector = pathlib.Path(app_data,"thridparty","authlib-injector.jar")

def get_system_arch():
    if arch.lower() == "amd64":
        return "x64"
    elif arch.lower() == "aarch64":
        return "arm64"
    elif arch.lower() == "i386":
        return "x86"
    return ""

config = app_data + "/config/launcher.yml"

config_provider = ConfigProvider.File

context = ssl.create_default_context(cafile=certifi.where()) if os.getenv("MIRAICL_ENSURE_SECURE_SSL") else ssl.create_default_context()

cache_response_data_path = pathlib.Path(app_data + "/cache/web/request.json")

if not cache_response_data_path.exists():
    cache_response_data_path.parent.mkdir(parents=True,exist_ok=True)
    cache_response_data_path.touch()

data_handle_obj = cache_response_data_path.open("r+")

cache_responses = get_jtoken(data_handle_obj.read())