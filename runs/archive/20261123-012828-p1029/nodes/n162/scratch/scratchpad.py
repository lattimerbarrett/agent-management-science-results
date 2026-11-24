from pathlib import Path
root=Path('experiments')
print('Experiment directories:', [str(p) for p in root.iterdir()] if root.exists() else 'not present')
if root.exists():
    for p in root.rglob('*.md'):
        if any(s in p.name.lower() for s in ('completion', 'reduction', 'proof')):
            print('\nFILE',p)
            text=p.read_text(errors='replace')
            lines=text.splitlines()
            hits=[i for i,l in enumerate(lines) if any(s in l.lower() for s in ('monotone complete', 'monotone sequential', 'sait', 'wright', 'theorem', 'normal aw'))]
            for i in hits[:12]:
                print('\n'.join(lines[max(0,i-1):min(len(lines),i+3)]))
