from pathlib import Path
for d in ['e1','e2','e3','e4']:
    for p in Path('experiments',d).rglob('*'):
        if p.is_file() and p.suffix in ['.md','.txt']:
            text=p.read_text(errors='replace')
            for line in text.splitlines():
                if any(w in line.lower() for w in ['kaplansky','sait','wright','berberian','open problem','open whether']):
                    print(str(p)+': '+line[:1000])
