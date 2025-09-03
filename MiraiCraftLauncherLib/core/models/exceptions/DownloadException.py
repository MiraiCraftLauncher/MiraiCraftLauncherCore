class DownloadException(Exception):
    def __init__(self,msg:str,ex_per_source:list[Exception] = [],caused:Exception = None):
        #super(msg)
        pass
    @staticmethod
    def throw_if_not_source(source:list,filename:str):
        if not source:
            raise DownloadException(f"文件 {filename} 无可用下载源")
        return source[0]