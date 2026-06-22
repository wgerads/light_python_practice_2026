import os

def scan_recursive(directory_path):
    """Рекурсивный обход """
    files_info = []
    
    try:
        items = os.listdir(directory_path)
        
        for item in items:
            full_path = os.path.join(directory_path, item)
            
            if os.path.isfile(full_path):
                stat = os.stat(full_path)
                files_info.append({
                    'path': full_path,
                    'size': stat.st_size,
                    'modified': stat.st_mtime
                })
            elif os.path.isdir(full_path):
                files_info.extend(scan_recursive(full_path))
                
    except PermissionError:
        print(f"Нет доступа к {directory_path}")
    
    return files_info
