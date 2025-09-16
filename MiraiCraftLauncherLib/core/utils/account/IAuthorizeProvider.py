class IAuthorizeProvider:
    """身份认证提供程序的基类"""
    def __init__(self):
        pass
    async def authenticate(self):
        pass
    async def refresh():
        pass
    async def validate():
        pass
    async def invalidate():
        pass