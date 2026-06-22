import os
import sys
from scanner import scan_recursive

# ============ ПАРАМЕТРЫ ============

# Значения по умолчанию
path = os.getcwd()
ext = None
min_size = None

# Разбираем команду
args = sys.argv[1:]
i = 0

while i < len(args):
    if args[i] == '-h':
        print("\n📁 СКАНЕР ФАЙЛОВ")
        print("  python main.py [ПАПКА] [-e .py] [-s 1]")
        print("\n  -e .py   фильтр по расширению")
        print("  -s 1     минимальный размер в МБ")
        print("  -h       справка")
        sys.exit(0)
    
    elif args[i] == '-e':
        ext = args[i + 1]
        i += 2
    
    elif args[i] == '-s':
        min_size = float(args[i + 1])
        i += 2
    
    else:
        if os.path.isdir(args[i]):
            path = args[i]
        i += 1

# ============ СКАНИРУЕМ ============

print(f"\n📁 Папка: {path}")
files = scan_recursive(path)
print(f"✅ Найдено: {len(files)} файлов")

# ============ ФИЛЬТРЫ ============

if ext:
    if not ext.startswith('.'):
        ext = '.' + ext
    files = [f for f in files if f['path'].lower().endswith(ext.lower())]
    print(f"🔍 Фильтр {ext}: {len(files)} файлов")

if min_size:
    min_bytes = min_size * 1024 * 1024
    files = [f for f in files if f['size'] >= min_bytes]
    print(f"🔍 Фильтр > {min_size} МБ: {len(files)} файлов")

# ============ ВЫВОД ============

if not files:
    print("❌ Файлов нет")
    sys.exit(0)

# Сортируем по размеру
files.sort(key=lambda x: x['size'], reverse=True)

print("\n" + "=" * 60)
print(f"{'№':<4} {'МБ':<8} {'Имя файла'}")
print("=" * 60)

for i, f in enumerate(files[:20], 1):
    name = os.path.basename(f['path'])
    mb = f['size'] / (1024 * 1024)
    print(f"{i:<4} {mb:<8.2f} {name}")

print("=" * 60)

total_mb = sum(f['size'] for f in files) / (1024 * 1024)
print(f"\n📊 Всего: {len(files)} файлов, {total_mb:.2f} МБ")
