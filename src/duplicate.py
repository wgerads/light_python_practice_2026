import hashlib

def calculate_sha256(filepath):
    """Cчитает хеш файла блоками по 64 КБ."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, PermissionError):
        return None

def extract_duplicates(hash_map):
    """Оставляет в словаре ТОЛЬКО те хеши, где путей больше или равно 2."""
    duplicates = {}
    for file_hash, paths in hash_map.items():
        if len(paths) >= 2: 
            duplicates[file_hash] = paths
    return duplicates
