from enum import Enum
from typing import Optional
import asyncio
import time
import threading
import random

class LoaderStatus(Enum):
    Pending = 0
    Processing = 1
    Complete = 2
    Failed = 3
    ParallelComplete = 4
    Canceled = 5

class LoaderInput:
    def __init__(self,data):
        self.data = data
        self._stop_event = threading.Event()
        self.identifier = ""

class LoaderTask:
    def __init__(self,method):
        self.method = method
        self.name = "未命名加载器"
        self.input:Optional[LoaderInput] = None
        self.status = LoaderStatus.Pending
        self.task:Optional[asyncio.Task] = None
        self.expire_at = None
    def acquire_input(self,input:LoaderInput):
        self.input = input
        self.input.identifier = self.name
    async def start(self,is_force_start = False):
        if (self.expire_at and time.time() < self.expire_at) and (self.status == LoaderStatus.Processing and self.task):
            if is_force_start:
                self.task.cancel()
            return
        self.task = asyncio.create_task(self.method(self.input))
    def cancel(self):
        if self.task and not self.task.done():
            self.task.cancel()
    async def wait_for_result(self):
        if self.task:
            await self.task
    
class LoaderMultipleTask:
    def __init__(self,loaders:list[LoaderTask]):
        self.name = "未命名加载器"
        self.status = LoaderStatus.Pending
        self.expire_at = None
        self.loop = None
        self.loaders = loaders
        self.tasks = []
    async def start(self,is_force_start=False):
        if (self.expire_at and time.time() < self.expire_at) and (self.status == LoaderStatus.Processing and self.loaders):
            if not is_force_start:
                return
        for loader in self.loaders:
            await loader.start(is_force_start)
            self.tasks.append(asyncio.create_task(loader.wait_for_result()))
        return await asyncio.gather(*self.tasks)