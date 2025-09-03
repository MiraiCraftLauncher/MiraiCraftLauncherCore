import secrets

def get_encrypt_safe_random_int(length:int = 5):
    if length <= 0:
        raise ValueError(f"Invalid length: {length}")
    return secrets.randbelow(10 * length -1) + 10 * length - 1