from enum import Enum
from platform import system

class SystemType(Enum):
    Unknown = 0
    Windows = 1
    Linux = 2
    macOS = 3

system_name = system()

def get_os_type():
    if "win" in system_name.lower():
        return SystemType.Windows
    elif "osx" in system_name.lower() or "macos" in system_name.lower():
        return SystemType.macOS
    else:
        return SystemType.Linux

system_type = get_os_type()

def get_system_type():
    os_name = system_name.lower()
    if "win" in os_name:
        return SystemType.Windows
    elif "lix" in os_name or "linux" in os_name:
        return SystemType.Linux
    elif "osx" in os_name or "mac" in os_name:
        return SystemType.macOS
    return SystemType.Unknown