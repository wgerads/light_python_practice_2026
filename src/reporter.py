import os

def print_duplicates_report(duplicates):
    print("\n" + "=" * 30)
    print("ОТЧЕТ ПО ДУБЛИКАТАМ:")
    print("=" * 30)
    
    if not duplicates:
        print("Повторяющихся файлов не обнаружено.")
        return

    for hash_str, paths in duplicates.items():
        print(f"\nОбнаружены дубликаты (Хэш: {hash_str[:10]}...):")
        for path in paths:
            print(f" -> {path}")

def print_backup_compare_report(source_raw, backup_raw, source_dir, backup_dir):
    """Этап 4: Сравнивает исходную папку с бэкапом на основе собранных хешей."""
    print("\n" + "=" * 30)
    print("ОТЧЕТ О РЕЗЕРВНОЙ КОПИИ:")
    print("=" * 30)

    # Перестраиваем словари из {хеш: [пути]} в {относительный_путь: хеш}
    def to_rel_map(raw_map, base_dir):
        rel_map = {}
        for f_hash, paths in raw_map.items():
            for p in paths:
                rel_path = os.path.relpath(p, base_dir)
                rel_map[rel_path] = f_hash
        return rel_map

    src_map = to_rel_map(source_raw, source_dir)
    bak_map = to_rel_map(backup_raw, backup_dir)

    missing = []
    modified = []
    extra = []

    # Проверяем файлы из источника
    for rel_path, src_hash in src_map.items():
        if rel_path not in bak_map:
            missing.append(rel_path)
        elif src_hash != bak_map[rel_path]:
            modified.append(rel_path)

    # Проверяем лишние файлы в бэкапе
    for rel_path in bak_map:
        if rel_path not in src_map:
            extra.append(rel_path)

    # Вывод результатов
    print(f"\n[Отсутствуют в бэкапе]: {len(missing)} шт.")
    for f in sorted(missing): print(f" -> {f}")

    print(f"\n[Изменены]: {len(modified)} шт.")
    for f in sorted(modified): print(f" -> {f}")

    print(f"\n[Лишние в бэкапе]: {len(extra)} шт.")
    for f in sorted(extra): print(f" -> {f}")
