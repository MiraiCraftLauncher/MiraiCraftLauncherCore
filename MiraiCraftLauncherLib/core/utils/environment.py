app_debug = True

minecraft_folder ={
    "current":{
        "name":"launcher.minecraft.path.default",
        "path":{
            "condition":{
                "on-all-os":".",
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