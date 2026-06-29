import sys
import os
from scanner import scan_directory      
from duplicate import extract_duplicates
from reporter import print_duplicates_report, print_backup_compare_report

def check_arguments():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Использование для дубликатов: python main.py [папка] [расширение]")
        print("Использование для бэкапа:     python main.py [папка_источник] [папка_бэкап]")
        sys.exit(1)
        
    return sys.argv[1:]

def main():
    args = check_arguments()
    
    # Сравнение исходной папки и бэкапа (
    if len(args) == 2 and os.path.isdir(args[0]) and os.path.isdir(args[1]):
        source_dir, backup_dir = args[0], args[1]
        
        print(f"Старт анализа источника: {source_dir}")
        source_raw = scan_directory(source_dir)
        
        print(f"\nСтарт анализа бэкапа: {backup_dir}")
        backup_raw = scan_directory(backup_dir)
        
        print_backup_compare_report(source_raw, backup_raw, source_dir, backup_dir)
        
    # Поиск дубликатов 
    else:
        path = args[0]
        extension = args[1] if len(args) == 2 else None
    
        if extension:
    if extension in [".", "/.", ""]:
        extension = None
    else:
        if not extension.startswith("."):
            extension = "." + extension
        
        if not os.path.isdir(path):
            print(f"Ошибка: Путь {path} не существует или не является папкой.")
            sys.exit(1)
            
        print(f"Старт анализа папки: {path}")
        if extension:
            print(f"Фильтр по расширению: {extension}")
        print("-" * 30)

        raw_results = scan_directory(path, extension=extension)
        duplicates = extract_duplicates(raw_results)
        print_duplicates_report(duplicates)

if __name__ == "__main__":
    main()
