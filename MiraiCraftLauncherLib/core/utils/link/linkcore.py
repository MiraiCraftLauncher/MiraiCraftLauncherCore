from MiraiCraftLauncherLib.core.utils.system.text import secret,base32
from MiraiCraftLauncherLib.core.utils.system.os.process import Process

LOBBY_HOST_IP = "10.201.207.12"

class LinkLobby:
    def __init__(self,lobby_code:str = ""):
        # create a new link lobby
        if lobby_code:
            # Mirai CL lobby code
            if lobby_code.isdigit():
                if len(lobby_code) > 15 or len(lobby_code) < 13:
                    raise ValueError("Invalid MiraiCL lobby code")
                self.lobby_code = [lobby_code[:4],lobby_code[4:9],lobby_code[9:]]
            # PCL CE lobby Code
            elif len(lobby_code) < 9:
                self.lobby_code = [base32.Base32.decode_number(lobby_code)]
            # Terracotta code
            else:
                self.lobby_code = lobby_code.split("-")
                if len(self.lobby_code) < 5:
                    raise ValueError("Invalid Terracotta code")
    def start_lobby(self):
        Process()