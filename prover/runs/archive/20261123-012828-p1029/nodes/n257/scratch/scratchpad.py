from pathlib import Path
terms=['sait','berberian','sequentially complete','sequential completeness','wright','kaplansky']
for p in Path('experiments').rglob('*.md'):
 text=p.read_text(errors='replace')
 matches=[(i,line) for i,line in enumerate(text.splitlines(),1) if any(t in line.lower() for t in terms)]
 if matches:
  print('\n'+str(p))
  for i,line in matches[:12]: print(f'{i}: {line}')
print('\nDefinition check for the supplied theorem:')
print('AW*: a unital C*-algebra whose right annihilator of every subset is projection-generated.')
print('Factor: center is C1.')
print('Finite: the unit projection is not equivalent to a proper subprojection, equivalently every isometry is unitary.')
print('The problem explicitly supplies all three hypotheses.')
print('The sequence is increasing and norm-bounded by 1, so monotone sequential completeness gives its least upper bound in M_sa.')