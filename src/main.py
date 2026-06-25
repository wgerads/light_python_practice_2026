    import sys
    import os

    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")

    from scanner import scan_directory
    from reporter import print_duplicates_report
    from comparator import compare_directories  

    def check_arguments():
        if len(sys.argv) < 3:
            target_path = sys.argv[1] if len(sys.argv) == 2 else "."
            
            if not os.path.exists(target_path) or not os.path.isdir(target_path):
                print(f"Ошибка: Путь '{target_path}' не существует или не является папкой.")
                sys.exit(1)
                
            return "duplicates", target_path, None
        else:
            source_path = sys.argv[1]
            backup_path = sys.argv[2]
            
            for path, name in [(source_path, "Исходная папка"), (backup_path, "Папка бэкапа")]:
                if not os.path.exists(path) or not os.path.isdir(path):
                    print(f"Ошибка: {name} '{path}' не существует или не является директорией.")
                    sys.exit(1)
                    
            return "compare", source_path, backup_path

    def main():
        mode, path1, path2 = check_arguments()
        
        if mode == "duplicates":
            print(f"Старт анализа папки: {path1}")
            print("-" * 30)
            results = scan_directory(path1)
            print_duplicates_report(results)
            
        elif mode == "compare":
            print(f"Старт сравнения директорий...")
            print(f"Источник: {path1}")
            print(f"Бэкап:    {path2}")
            print("-" * 50)
            
            missing, modified, extra = compare_directories(path1, path2)
            
            print("\n" + "=" * 50)
            print("                 ОТЧЕТ О РАЗЛИЧИЯХ")
            print("=" * 50)
            
            print(f"\n ОТСУТСТВУЮТ В БЭКАПЕ (Всего: {len(missing)}):")
            if missing:
                for f in sorted(missing): print(f"  - {f}")
            else:
                print("  (нет отсутствующих файлов)")
                
            print(f"\n️ ИЗМЕНЕННЫЕ ФАЙЛЫ (Всего: {len(modified)}):")
            if modified:
                for f in sorted(modified): print(f"  - {f}")
            else:
                print("  (нет измененных файлов)")
                
            print(f"\n ЛИШНИЕ ФАЙЛЫ В БЭКАПЕ (Всего: {len(extra)}):")
            if extra:
                for f in sorted(extra): print(f"  - {f}")
            else:
                print("  (нет лишних файлов)")
                
            print("\n" + "=" * 50)

    if __name__ == "__main__":
        main()
