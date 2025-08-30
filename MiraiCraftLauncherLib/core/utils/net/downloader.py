import asyncio

current_thread_count = 64

class NetFile:
    def __init__(self,sources:list[str],path:str,start_size:int,end_size:int,algorithm:str,hash:str):
        self.sources = sources
        self.path = path
        self.start_position = start_size
        self.end_position = end_size
        self.algorithm = algorithm
        self.hash = hash
        self.is_spilted = False
        self.total_size = end_size - start_size
    async def download(self):
        """启动一个协程下载文件"""
        pass
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

class NetTask:
    pass