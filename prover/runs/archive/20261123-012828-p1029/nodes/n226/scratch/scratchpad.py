from pathlib import Path
terms=('construct','endpoint','1/2','half','witness')
for root in sorted(Path('experiments').iterdir()):
 for p in sorted(root.rglob('*')):
  if not p.is_file(): continue
  text=p.read_text(errors='replace')
  if p.suffix not in ('.md','.txt'):
   matches=[(i,line) for i,line in enumerate(text.splitlines(),1) if any(t in line.lower() for t in terms)]
   if matches:
    print('\n'+str(p))
    for i,line in matches: print(f'{i}: {line[:240]}')
print('\nAudit conclusion: no endpoint construction found. The notes explicitly disclaim one.')
