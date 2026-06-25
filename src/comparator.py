import os
import hashlib

def calculate_sha256(filepath):
    """Побайтовое чтение файла для точного расчета хэша."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):                  sha256.update(chunk)
        return sha256.hexdigest()
    except (OSError, PermissionError):
        return "ERROR_READ"

def scan_directory_for_diff(target_path):
    """Низкоуровневое сканирование папки для сравнения структур."""
    results = {}
    base_abs = os.path.abspath(target_path)
    
    for root, _, files in os.walk(base_abs):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_abs)
            try:
                stat_info = os.stat(full_path)
                size = stat_info.st_size
                file_hash = calculate_sha256(full_path)
                results[rel_path] = (size, file_hash)
            except OSError:
                continue
    return results

def compare_directories(source_dir, backup_dir):
    """Основная функция сравнения, разделяющая файлы по трем категориям."""
    source_data = scan_directory_for_diff(source_dir)
    backup_data = scan_directory_for_diff(backup_dir)
    
    missing = []   
    modified = [] 
    extra = []     
    
    for rel_path, (src_size, src_hash) in source_data.items():
        if rel_path not in backup_data:
            missing.append(rel_path)
        else:
            bak_size, bak_hash = backup_data[rel_path]
            if src_size != bak_size or src_hash != bak_hash:
                modified.append(rel_path)
                
    for rel_path in backup_data:
        if rel_path not in source_data:
            extra.append(rel_path)
            
    return missing, modified, extra
