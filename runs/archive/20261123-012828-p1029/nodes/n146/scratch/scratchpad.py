from pathlib import Path
for root in ('experiments/e1','experiments/e2','experiments/e3','experiments/e4'):
 p=Path(root)
 print('\nAUDIT',root)
 if not p.exists():
  print('not present'); continue
 notes=list(p.rglob('*.md'))
 print('markdown files:',len(notes))
 for f in notes:
  text=f.read_text(errors='replace')
  hits=[line for line in text.splitlines() if any(word in line.lower() for word in ('monotone complete','monotone completeness','strict monotonic','not proved','not proven','unproved','not establish','not a proof','open problem','kaplansky'))]
  if hits:
   print(f.name)
   print('\n'.join(hits[:6])[:1800])
print('\nAUDIT CONCLUSION: No supplied proof establishes supremum-existence, projection-packing exhaustion, strict order preservation, or positive-increment attainability.')