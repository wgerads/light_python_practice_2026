def print_duplicates_report(hash_map):
    print("\n" + "=" * 30)
    print("ОТЧЕТ ПО ДУБЛИКАТАМ:")
    print("=" * 30)
    
    duplicates_found = False
    
    for hash_str, paths in hash_map.items():
        if len(paths) >= 2:
            duplicates_found = True
            print(f"\nОбнаружены дубликаты (Хэш: {hash_str[:10]}...):")
            for path in paths:
                print(f"  -> {path}")
                
    if not duplicates_found:
        print("Повторяющихся файлов не обнаружено.")
