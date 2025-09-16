from loguru import logger
from MiraiCraftLauncherLib.core.utils.environment import app_debug
import sys

logger.remove()

if app_debug:
    logger.add(
        sys.stdout,
        level="TRACE"
    )


logger.add(
    "logs/app.log",
    rotation="100 MB",
    retention="30 days",  
    compression="zip",    
    encoding="utf-8",     
    level="INFO"         
)

def debug(module:str,message:str):
    logger.debug(f"[{module}] {message}")

def info(module:str,message:str):
    logger.info(f"[{module}] {message}")

def warning(module:str,message:str):
    logger.warning(f"[{module}] {message}")

def error(module:str,message:str):
    logger.opt(exception=True).error(f"[{module}] {message}")

def fatal(module:str,message:str):
    logger.exception(f"[{module}] {message}")
    sys.exit(1)

