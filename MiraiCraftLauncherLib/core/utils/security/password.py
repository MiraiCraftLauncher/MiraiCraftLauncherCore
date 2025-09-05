import keyring

def get_password(user:str):
    return keyring.get_password("MiraiCL",user)

def update_password(user:str,password:str):
    keyring.set_password("MiraiCL",user,password)

def delete_password(user:str):
    keyring.delete_password("MiraiCL",user)

    