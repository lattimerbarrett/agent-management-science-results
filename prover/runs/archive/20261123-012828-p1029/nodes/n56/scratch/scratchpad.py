from pathlib import Path
terms=('modulus','strict order','uniform strict','exhaustion','cauchy theorem')
for root in ('experiments/e1','experiments/e2','experiments/e3'):
    for p in Path(root).rglob('*.md'):
        lines=p.read_text(errors='replace').splitlines()
        for i,line in enumerate(lines):
            if any(term in line.lower() for term in terms):
                print(f'{p}:{i+1}: {line}')
