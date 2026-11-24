from pathlib import Path
for d in ['experiments/e1','experiments/e4']:
 print(d)
 for f in Path(d).glob('*'):
  if f.is_file() and f.suffix in ['.md','.txt']:
   s=f.read_text(errors='replace')
   if any(t in s.lower() for t in ['sait','wright','berberian','monotone completeness']):
    print(f.name)
