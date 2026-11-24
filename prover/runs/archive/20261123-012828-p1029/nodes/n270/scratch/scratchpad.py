from pathlib import Path
# Audit available local proof notes for a bibliographic reference;
# this search is not a proof of the structural theorem.
files=[p for p in Path('experiments').rglob('*') if p.is_file()]
print('Available local experiment files:',len(files))
for p in files:
    if p.suffix in ('.md','.txt'):
        text=p.read_text(errors='replace')
        hits=[line for line in text.splitlines() if any(k in line.lower() for k in ('sequentially complete','sequential completeness','berberian','kaplansky','saito','saitô'))]
        if hits:
            print(p)
            print('\n'.join(hits[:8]))
print('\nPrecise theorem to apply: every norm-bounded increasing sequence in the self-adjoint part of a finite AW*-factor has a least upper bound there.')
print('For the proposed sequence: 0 <= a_n <= 1 gives norm boundedness, and a_n <= a_(n+1) gives increasingness.')
print('Therefore the theorem gives the very least upper bound whose absence is required.')
