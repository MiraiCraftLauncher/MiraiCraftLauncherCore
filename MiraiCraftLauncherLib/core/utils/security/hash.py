import hashlib
import pathlib

def calc_hash(hash_obj,file:str = None,data = None):
    if file:
        with pathlib.Path(file).open("rb") as f:
            while True:
                chunck = f.read(1024)
                if not chunck:
                    break
                hash_obj.update(chunck)
    elif data:
        if isinstance(data,str):
            hash_obj.update(data.encode())
        else:
            hash_obj.update(data)
    else:
        raise ValueError("Invalid input: must offer data or file path.")
    return hash_obj.hexdigest()

def md5(file:str = None,data = None):
    return calc_hash(hashlib.md5(),file,data)
def sha1(file:str = None,data = None):
    return calc_hash(hashlib.sha1(),file,data)
def sha256(file:str = None,data = None):
    return calc_hash(hashlib.sha256(),file,data)
def sha512(file:str = None,data = None):
    return calc_hash(hashlib.sha512(),file,data)

def murmur2(file:str = None,data = None):
    hash_data = 0
    valid_length = 0
    with pathlib.Path(file).open("rb") as f:
        while True:
            chunck = f.read(16384)
            for byte in chunck:
                if byte in [9,10,13,32]:
                    continue
                valid_length +=1
            if not chunck:
                break
        f.seek(0)
        seed = (1 ^ valid_length)
        while True:
            chunck = f.read(16384)
            for byte in chunck:

            