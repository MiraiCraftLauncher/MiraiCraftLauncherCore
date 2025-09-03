import platform
import os
import pathlib
app_debug = True

minecraft_folder ={
    "current":{
        "name":"launcher.minecraft.path.default",
        "path":{
            "condition":{
                "on-all-os":"${appenv:executable_path}",
            }
        },
        "versions":[],
    },
    "official":{
        "name":"launcher.minecraft.path.official",
        "path":{
            "condition":{
                "on-windows":{
                    "path":"${osenv:appdata}/.minecraft"
                },
                "on-other":{
                    "path":"${path:linux_user_home}/.minecraft"
                },
            }
        },
        "versions":[]
    }
}

easy_tier_path = "${appenv:application_data}"

def get_full_path(path:str):
    return pathlib.Path(path.replace("${osenv:appdata}",os.getenv("appdata")).replace("${path:linux_user_home}","~").replace("${appenv:application_data}",""))