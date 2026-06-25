import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from scanner import scan_directory
from reporter import print_duplicates_report

def check_arguments():
    if len(sys.argv) < 2:
        print("Ошибка: Не указан путь к папке.")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    if not os.path.exists(target_path) or not os.path.isdir(target_path):
        print(f"Ошибка: Путь '{target_path}' не существует или не является папкой.")
        sys.exit(1)
        
    return target_path

def main():
    folder_to_scan = check_arguments()
    print(f"Старт анализа папки: {folder_to_scan}")
    print("-" * 30)
    
    # 1. Собираем результаты в словарь
    results = scan_directory(folder_to_scan)
    
    # 2. Передаем словарь в модуль отчета
    print_duplicates_report(results)

if __name__ == "__main__":
    main()
