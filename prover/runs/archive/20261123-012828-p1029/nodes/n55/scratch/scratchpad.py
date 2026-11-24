from pathlib import Path
# Audit the available notes for a precise theorem name/reference.
keywords = ('sait', 'berberian', 'kaplansky', 'sequential completeness theorem')
for p in Path('experiments').rglob('*.md'):
    text = p.read_text(errors='replace')
    hits = [(i,line) for i,line in enumerate(text.splitlines(),1)
            if any(k in line.lower() for k in keywords)]
    if hits:
        print(p)
        for i,line in hits[:12]: print(f'{i}: {line}')
