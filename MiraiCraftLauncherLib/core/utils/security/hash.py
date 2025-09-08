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

def murmur2(file:str):
    """用于计算 Mod Hash （非标准 Murmur Hash 2）"""
    with pathlib.Path(file).open("rb") as f:
        # 计算长度
        valid_length = 0
        while True:
            chunk = f.read(16384)
            if not chunk:
                break
            for byte in chunk:
                if byte not in [9, 10, 13, 32]:  # 排除制表符、换行符、回车符、空格
                    valid_length += 1
        # 1 是种子
        # 对计算结果进行截断，避免 uint32 被转换成 uint64
        h = (1 ^ valid_length) & 0xFFFFFFFF
        buffer = bytearray()
        
        f.seek(0)  
        while True:
            chunk = f.read(16384)
            if not chunk:
                break
                
            # 过滤换行、制表符、空格等
            # 不过滤会导致最终算出来的 hash 与实际的 hash 不一样
            for byte in chunk:
                if byte not in [9, 10, 13, 32]:
                    buffer.append(byte)
            
            while len(buffer) >= 4:
                # 确保是小序端排列
                k = buffer[0] | (buffer[1] << 8) | (buffer[2] << 16) | (buffer[3] << 24)
                
                # 对结果添加扰动
                k = (k * 0x5BD1E995) & 0xFFFFFFFF
                k ^= k >> 24
                k = (k * 0x5BD1E995) & 0xFFFFFFFF
                h = (h * 0x5BD1E995) & 0xFFFFFFFF
                h ^= k
                
                del buffer[:4]
        
        # 末尾处理
        remaining = len(buffer)
        if remaining > 0:
            k = 0
            if remaining >= 3:
                k ^= buffer[2] << 16
            if remaining >= 2:
                k ^= buffer[1] << 8
            if remaining >= 1:
                k ^= buffer[0]
            
            k = (k * 0x5BD1E995) & 0xFFFFFFFF
            h ^= k
        
        # 混合
        h ^= h >> 13
        h = (h * 0x5BD1E995) & 0xFFFFFFFF
        h ^= h >> 15
        
        return h