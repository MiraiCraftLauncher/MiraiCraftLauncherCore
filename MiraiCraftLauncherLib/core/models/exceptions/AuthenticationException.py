from enum import Enum

class AuthenticationErrorType(Enum):
    AccessDenied = 0
    RequiredRelogin = 1
    IncorrectUsernameOrPassword = 2
    AccountLoginProhibited = 3
    InternalError = 4
    Unsupported = 5
    Unknown = 6


class AuthenticationException(Exception):
    def __init__(self, msg: str = None,err_code:AuthenticationErrorType = AuthenticationErrorType.Unknown):
        
        super().__init__()