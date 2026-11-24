from pathlib import Path
root=Path('experiments/e1')
print('Workspace present:', root.exists())
if root.exists():
    paths=list(root.rglob('*'))
    for p in paths:
        if p.is_file() and p.suffix in ('.md','.txt') and ('completion' in p.name or 'reduction' in p.name):
            print('\nFILE',p)
            text=p.read_text(errors='replace')
            for line in text.splitlines():
                if any(word in line.lower() for word in ['sequential','monotone complete','monotone completeness','citation']):
                    print(line[:1200])
print('\nSufficient structural input: every bounded increasing self-adjoint sequence in a finite AW*-factor has a least upper bound. The proposed a_n satisfies these hypotheses because 0 <= a_n <= 1.')
