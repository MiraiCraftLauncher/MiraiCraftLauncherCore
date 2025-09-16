try:
    import winreg
except:
    pass

import yaml
from MiraiCraftLauncherLib.core.utils.environment import config,system_type,SystemType,config_provider,ConfigProvider
from MiraiCraftLauncherLib.core.models.account.authmethod import AuthMethod
from MiraiCraftLauncherLib.core.utils.runtime import logger


# 设置项
class SetupBase():
    def __init__(self):
        self.init()
        self.origin = self.__dict__.copy()
    def init():
        pass
    def update():
        pass
    """所有设置项的基类"""
    def save():
        pass
    def reset(self):
        self.__dict__.clear()
        self.__dict__.update(self.origin)
SetupBase.__dict__

class SystemSetup(SetupBase):
    def init(self):
        self.proxy = ""
        self.argee_eula = False
        self.argee_tof = False
        self.current_minecraft_folder = None
        self.custom_argument = []
        self.window_title = None
        self.theme = None
        self.update_server = None
        self.java = None

class VersionSetup(SetupBase):
    def init(self):
        self.path = None
        self.custon_argument = None
        self.use_http_proxy = None
        self.allow_login_method = AuthMethod.Undefined
        self.auth_server_root = ""
        self.enable_version_indie = True
        self.in_favorites = False
        self.modable = False
        self.release_mode = True
        self.disallow_update = False
        self.select_java = None
        self.minium_java_version = None
        self.disable_file_check = False
        self.last_launch = None
        self.spent_time = None
        self.command_before_launch = None
        self.perfer_profile = None
        self.show_name = None


def load_config():
    try:
        if system_type == SystemType.Windows and config_provider == ConfigProvider.Registry:
            return winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,"Software\\LuoYun-Team\\MiraiCL",access=winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY)
        else:
            with open("","r") as f:
                return yaml.load(f)
    except:
        logger.error("Setup","打开配置文件失败")

config = load_config()

versions = []

profile = None

system = SystemSetup()