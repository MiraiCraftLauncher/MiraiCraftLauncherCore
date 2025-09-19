import socket
import asyncio


class WebServer:
    def __init__(self,addr:list[str] = ["127.0.0.1"],port:int = 8000):
        self.addr = addr
        self.port = port
        self.http_handle_mapping = {}
        self.ws_handle_mapping = {}
    async def startup(self):
        pass
    async def shutdown(self):
        pass
    def add_path_handle():
        pass
    def handle_http_request_notfound():
        pass