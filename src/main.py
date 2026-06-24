import sys
import os

def check_arguments():
    # Проверяем наличие аргумента командной строки
    if len(sys.argv) < 2:
        print("Ошибка: Не указан путь к папке.")
        print("Использование: python script.py <путь_к_папке>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    # Проверяем существование пути и что это директория
    if not os.path.exists(target_path):
        print(f"Ошибка: Путь '{target_path}' не существует.")
        sys.exit(1)
        
    if not os.path.isdir(target_path):
        print(f"Ошибка: Путь '{target_path}' не является папкой.")
        sys.exit(1)
        
    return target_path

def scan_directory(current_dir, depth=0):
    try:
        # Получаем список всех элементов в текущей папке
        items = os.listdir(current_dir)
    except PermissionError:
        # Обрабатываем папки, к которым нет доступа
        indent = "  " * depth
        print(f"{indent}[Доступ ограничен] {os.path.basename(current_dir)}")
        return

    for item in items:
        # Создаем полный путь к элементу
        full_path = os.path.join(current_dir, item)
        indent = "  " * depth
        
        if os.path.isdir(full_path):
            # Если это папка, выводим её имя и заходим внутрь 
            print(f"{indent} {item}/")
            scan_directory(full_path, depth + 1)
        else:
            print(f"{indent} {item}")

def main():
    # Этап 1: Проверка запуска и аргументов
    folder_to_scan = check_arguments()
    print(f"Старт анализа папки: {folder_to_scan}\n")
    
    # Этап 2: Рекурсивный обход и вывод структуры
    scan_directory(folder_to_scan)

if __name__ == "__main__":
    main()
