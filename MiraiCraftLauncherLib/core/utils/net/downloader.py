import asyncio
import pathlib
from MiraiCraftLauncherLib.core.utils.net.web import client

current_thread_count = asyncio.Semaphore(64)

class NetFile:
    def __init__(self,sources:list[str],path:str,start_size:int,end_size:int,algorithm:str,hash:str):
        self.sources = sources
        self.path = pathlib.Path(path)
        self.start_position = start_size
        self.end_position = end_size
        self.algorithm = algorithm
        self.hash = hash
        self.is_spilted = False
        self.total_size = end_size - start_size
        self.file_objs:list[NetFile] = []
    async def download(self):
        """启动一个协程下载文件"""
        async with current_thread_count:
            for source_url in self.sources:
                async with client.request("GET",source_url) as response:
                    with self.path.open("wb") as f:
                        for chunck in response.content.iter_chunked(16384):
                            f.write(chunck)
    def get_spilt(self) -> list:
        """获取 NetFile 的分片"""
        split_size = self.end_position // current_thread_count
        size_left = self.end_position % current_thread_count
        tasks = []
        if self.is_spilted or self.total_size < 512 * 1024:
            tasks.append(self)
            return tasks
        for file_spilt_count in range(current_thread_count):
            current_size = split_size * file_spilt_count
            file_obj = NetFile(
                sources = self.sources,
                path=self.path + f".tmp_{file_spilt_count}",
                start_size=current_size,
                end_size=current_size + split_size,
                algorithm="",
                hash=""
            )
            file_obj.is_spilted = True
            tasks.append(file_obj)
            self.file_objs = tasks
            return tasks
        if size_left:
            file_obj = NetFile(
                sources = self.sources,
                path=self.path + f".tmp_{self.end_position // current_thread_count + 1}",
                start_size=self.total_size - size_left,
                end_size=self.total_size,
                algorithm="",
                hash=""
            )
        return tasks
    def merge_file(self):
        with self.path.open("wb") as f:
            for file in self.file_objs:
                with file.path.open("rb") as file_spilt:
                    while True:
                        chunck = file_spilt.read(16384)
                        if not chunck:
                            break
                        f.write(chunck)
                    file.path.unlink(True)
    
            

class NetTask:
    def __init__(self,tasks:list[NetFile]):
        self.tasks = tasks
    def try_download(self):
        pass