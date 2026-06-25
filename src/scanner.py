
import os
import hashlib

def calculate_file_hash(file_path):
    """Счетчик хэша SHA-256 для содержимого файла."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(65536):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None

def scan_directory(current_dir, hash_map=None, depth=0):

    if hash_map is None:
        hash_map = {}

    try:
        items = os.listdir(current_dir)
    except PermissionError:
        indent = "  " * depth
        print(f"{indent}[Доступ ограничен] {os.path.basename(current_dir)}")
        return hash_map

    for item in items:
        full_path = os.path.join(current_dir, item)
        indent = "  " * depth
        
        if os.path.isdir(full_path):
            print(f"{indent} {item}/")
            
            scan_directory(full_path, hash_map, depth + 1)
        else:
            print(f"{indent} {item}")
            file_hash = calculate_file_hash(full_path)
            
            if file_hash:
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(full_path)
                
 
    return hash_map
