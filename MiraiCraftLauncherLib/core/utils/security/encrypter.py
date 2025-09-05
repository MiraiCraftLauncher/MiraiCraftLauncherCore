from cryptography import *
from MiraiCraftLauncherLib.core.utils.environment import secret_path
from MiraiCraftLauncherLib.core.utils.security.password import *
import secrets
import json
import keyring
import getpass

encrypt_key = ""

iv = ""

encrypt_data = get_password(getpass.getuser())

if not encrypt_data:
    encrypt_key = secrets.token_urlsafe(32)
    iv = secrets.token_urlsafe(14)
    update_password(getpass.getuser(),f"{encrypt_key}@{iv}")
else:
    spilt_data = encrypt_data.split("@")
    encrypt_key = spilt_data[0]
    iv = spilt_data[1]