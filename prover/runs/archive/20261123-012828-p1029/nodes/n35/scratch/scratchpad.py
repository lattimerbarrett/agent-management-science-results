from pathlib import Path
for base in [Path('experiments/e1'),Path('experiments/e2')]:
 print('\n',base)
 for p in base.rglob('*'):
  if p.is_file() and any(s in p.name for s in ['reduction_notes','completion_audit','partial_proof','extremal_reduction']):
   print('\nFILE',p,'\n',p.read_text()[:30000])
