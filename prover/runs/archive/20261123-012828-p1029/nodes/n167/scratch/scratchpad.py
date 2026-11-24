from pathlib import Path
for f in Path('experiments/e1').glob('*.md'):
 print('\nFILE',f.name)
 for line in f.read_text().splitlines():
  if any(w in line.lower() for w in ['open problem','kaplansky','monotone complete','sequential complete','sait','wright','berberian','haagerup','bessel']): print(line)
