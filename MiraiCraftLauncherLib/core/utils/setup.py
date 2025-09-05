import yaml
from MiraiCraftLauncherLib.core.utils.environment import minecraft_folder

setup = {
    "SystemHttpProxy":{
        "value":None
    },
    "DownloadSource":{
        "value":[]
        },
    "SourcePrefer":{
        "value":None,
    },
    "UpdateServer":{
        "value":"",
    },
    "Profile":{
        "value":[],
    },
    "MinecraftFolder":{
        "value":[
            {
                "name":"launcher.",
                "locked":True,
                "hidden":False,
                "path":minecraft_folder
            }
        ]
    },
    "CustomCertificates":{
        "value":[]
    },
    "Versions":[]
}