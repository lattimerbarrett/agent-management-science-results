from pathlib import Path
p=Path('experiments/e3')
print('Available e3 files:')
for f in p.rglob('*'):
    if f.is_file():
        print(f)
        if f.name.endswith('.md'):
            print(f.read_text()[:18000])
