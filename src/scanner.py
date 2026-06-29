import os
from datetime import datetime  
from duplicate import calculate_sha256

def scan_directory(current_dir, hash_map=None, depth=0, extension=None):
    if hash_map is None:
        hash_map = {}

    if extension and depth == 0:
        extension = extension.lower()
        if not extension.startswith('.'):
            extension = '.' + extension

    try:
        items = os.listdir(current_dir)
    except PermissionError:
        indent = "  " * depth
        print(f"{indent}[Доступ ограничен] {os.path.basename(current_dir)}")
        return hash_map

    for item in sorted(items):
        if item == "__pycache__":
            continue
            
        full_path = os.path.join(current_dir, item)
        indent = "  " * depth

        if os.path.isdir(full_path):
            print(f"{indent}{item}/")
            hash_map = scan_directory(full_path, hash_map, depth + 1, extension)
        else:
            if extension:
                _, ext = os.path.splitext(item)
                if ext.lower() != extension:
                    continue

                        try:
                stat = os.stat(full_path)
                size = stat.st_size
                
                
                formatted_date = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M:%S')
                
                print(f"{indent}{item} ({size} байт, дата: {formatted_date})")
            except OSError:
                print(f"{indent}{item}")

            file_hash = calculate_sha256(full_path)
            if file_hash:
                hash_map.setdefault(file_hash, []).append(full_path)

    return hash_map
