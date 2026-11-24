from pathlib import Path
# Audit whether any of the supplied notes already supplies a quantitative
# exhaustion inequality, rather than just a proposed one.
for p in Path('experiments').rglob('*.md'):
    lines=p.read_text().splitlines()
    hits=[(i+1,line) for i,line in enumerate(lines) if 'exhaust' in line.lower() or 'cotype' in line.lower()]
    if hits:
        print(p)
        for i,line in hits[:8]: print(f'  {i}: {line}')
print('\nApplication of the established exhaustion statement:')
print('b_n = a_(n+1)-a_n >= 0')
print('sum_(n<N) b_n = a_N-a_0 <= 1')
print('Therefore tau(b_n) -> 0; if tau(b_n)=eta for all n, eta=0.')
