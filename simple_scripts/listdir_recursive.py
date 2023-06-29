from pathlib import Path

for p in Path('.').rglob('*'):
    print(p)