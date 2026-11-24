from pathlib import Path
root=Path('experiments')
print('Experiments available:', root.exists())
if root.exists():
    paths=list(root.rglob('*.md'))
    print('Markdown files:',len(paths))
    for p in paths:
        text=p.read_text(errors='replace')
        lines=text.splitlines()
        hits=[(i,line) for i,line in enumerate(lines) if ('sequential' in line.lower() or 'sait' in line.lower()) and ('complet' in line.lower() or 'theorem' in line.lower())]
        if hits:
            print('\nFILE',p)
            for i,line in hits[:8]:
                print('\n'.join(lines[max(0,i-1):min(len(lines),i+2)]))
