from loguru import logger
from MiraiCraftLauncherLib.core.utils.environment import app_debug
import sys

logger.remove()

if app_debug:
    logger.add(
        sys.stdout,
        level="DEBUG"
    )


logger.add(
    "logs/app.log",
    rotation="100 MB",
    retention="30 days",  
    compression="zip",    
    encoding="utf-8",     
    level="DEBUG"         
)