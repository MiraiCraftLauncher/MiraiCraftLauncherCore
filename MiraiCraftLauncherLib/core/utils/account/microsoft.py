from MiraiCraftLauncherLib.core.utils.net.web import request
from enum import Enum
from MiraiCraftLauncherLib.core.utils.net.web import open_in_web_browser


class LoginType(Enum):
    Aurhorize = 0
    DeviceCode = 1
    WAM = 2

async def login():

    pass

async def login_wam():
    pass

async def login_authorize():
    pass

async def login_device():
    pass

async def refresh():
    pass

async def login_authorize_self():
    open_in_web_browser()

async def login_device_self_1():
    pass

async def login_device_self_2():
    pass