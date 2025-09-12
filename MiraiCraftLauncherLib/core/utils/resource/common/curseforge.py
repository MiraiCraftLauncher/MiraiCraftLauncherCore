class CurseForgeClient:
    def __init__(self,api_key:str):
        if not api_key:
            raise ValueError("Invalid API Key")
        self.key = api_key
        self.base_addr = "https://api.curseforge.com/v1"

    async def search(self):
        pass