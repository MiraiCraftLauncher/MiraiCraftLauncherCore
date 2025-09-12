from aiohttp import web
import socket
from MiraiCraftLauncherLib.core.utils.runtime.logger import logger

app:web.Application = None
runner = None

support_method = {
    "GET":web.get,
    "POST":web.post,
    "HEAD":web.head
}

def get_or_init_webserver():
    global app
    if not app:
        app = web.Application()
    return app

def startup(required_port:int = None) -> int:
    global runner
    if required_port:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1",required_port))
            sock.close()
        except Exception as ex:
            logger.warning("[Net] 指定的端口已被使用，将使用随机端口启动 Web 服务器")
            required_port = 0
    else:
        required_port = 0
    runner = web.run_app(get_or_init_webserver(),host="localhost",port=required_port,runner=True)

def add_route(path:str,method:str,handler:function):
    app.add_routes([support_method.get(method.upper())(path,handler)])

async def shutdown():
    logger.info("[WebServer] 正在关闭 Web 服务器")
    await app.shutdown()