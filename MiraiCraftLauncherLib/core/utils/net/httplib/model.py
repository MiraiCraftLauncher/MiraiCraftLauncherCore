from enum import Enum

class WebResponse:
    def __init__(self,status_code:int,headers:dict[str,str]):
        pass

class HTTPVersion:
    def __init__(self,major_version:int,minnor_version:int):
        self.version = (major_version,minnor_version)

class SSLErrorType(Enum):
    Invalid = 0
    Expired = 1
    CommonNameMismatched = 2
    CertificateRevoked = 4
    SubjectAlternativeNameMismatched = 5
    InsecureAlgorithm = 6
    IncompletedTrustChain = 7
    ProtocolError = 8
    Nothing = 9
    
class WebContent:
    def __init__():
        pass

class StringContent(WebContent):
    pass

class ByteContent(WebContent):
    pass

class StreamContent(WebContent):
    pass