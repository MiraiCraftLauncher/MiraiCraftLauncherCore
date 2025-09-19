from model import SSLErrorType

class NetworkException(Exception):
    def __init__(self,msg):
        super().__init__(msg)

class SSLHandshakeException(NetworkException):
    def __init__(self,msg:str,error:SSLErrorType = None):
        pass