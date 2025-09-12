import stat
import platform
import os
import pathlib
import getpass
from MiraiCraftLauncherLib.core.utils.system.os.info import system_type,SystemType

app_debug = True

executable_path = ""

app_data = f"{executable_path}/data/{getpass.getuser()}" if SystemType.Windows == system_type else f"/etc/MiraiCL/{getpass.getuser()}/data"

minecraft_folder = os.getenv("appdata") if system_type == SystemType.Windows else pathlib.Path.home().joinpath(".minecraft")

easy_tier_path = f"{app_data}/link/core/easytier"

secret_path = pathlib.Path(f"{app_data}/secret")

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