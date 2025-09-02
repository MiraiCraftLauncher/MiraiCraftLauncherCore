import subprocess
import elevate
import ctypes
import os
import pathlib
import asyncio

class Process:
    def __init__(self,executable:str,arguments:list[str],output_encoding:str = "utf-8",use_shell_executable:bool = False):
        self._process = subprocess.Popen(arguments,executable=executable,encoding=output_encoding,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=use_shell_executable)
    async def setup_watcher(self,file_path:str = None,on_get_output_callback:function = None):
        file_obj = pathlib.Path(file_path).open("w") if file_path else None
        while not self._process.poll():
            if file_obj and self._process.stdout:
                file_obj.write(self._process.stdout)
            on_get_output_callback(self._process.stdout)
            
            await asyncio.sleep(1)
    async def stop(self):
        if self._process.poll():
            self._process.terminate()
            await asyncio.sleep(2.5)
            if self._process.poll():
                self._process.kill()

elevate.elevate()