from pathlib import Path
for root in [Path('experiments/e1'),Path('experiments/e2'),Path('experiments/e3')]:
 print('\nROOT',root)
 for f in root.rglob('*'):
  if f.is_file() and f.suffix in ['.md','.txt']:
   text=f.read_text(errors='replace')
   if any(w in text.lower() for w in ['sait','berberian','wright','monotone complete','sequentially complete','pedersen']):
    print('\nFILE',f)
    lines=text.splitlines()
    for i,l in enumerate(lines):
     if any(w in l.lower() for w in ['sait','berberian','wright','monotone complete','sequentially complete','pedersen']):print('\n'.join(lines[max(0,i-2):min(len(lines),i+4)]))
