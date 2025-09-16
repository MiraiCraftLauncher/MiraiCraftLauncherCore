from MiraiCraftLauncherLib.core.utils.setup import setup
from MiraiCraftLauncherLib.core.utils.minecraft.version import get_version_info_by_release_time
from MiraiCraftLauncherLib.core.utils.system.text.jtoken import to_jstring
from datetime import datetime
import pathlib
instances = []

async def load_instance():
    instances = setup.get("versions")

async def add_instance(jtoken:dict,path:pathlib.Path):
    version = {}
    version_info = get_version_info_by_release_time(jtoken.get("releaseTime"))
    if version_info:
        version["GameVersion"] = version_info.get("id")
    version["RequiredJava"] = jtoken.get("javaVersion").get("majorVersion")
    main_class = jtoken.get("mainClass")
    version["Subassembly"] = []
    jstring = to_jstring(jtoken)
    if "minecraftforge" in main_class:
        version["Subassembly"].append("Forge")
        version["Modable"] = True
    if "optifine" in jstring:
        version["Subassembly"].append("OptiFine")
    if "fabric" in main_class:
        version["Subassembly"].append("Fabric")
        version["Modable"] = True
    if "neoforge" in main_class:
        version["Subassembly"].append("NeoForge")
        version["Modable"] = True
    version["createTime"] = datetime.now()
    