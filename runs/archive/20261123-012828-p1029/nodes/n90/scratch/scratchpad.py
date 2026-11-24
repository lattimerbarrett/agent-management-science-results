from pathlib import Path
for root in ('experiments/e2','experiments/e3'):
 print('\nAUDIT',root)
 for p in Path(root).rglob('*.md'):
  text=p.read_text(errors='replace')
  lines=[line for line in text.splitlines() if any(term in line.lower() for term in ('construct','existence','witness','unproved','endpoint'))]
  if lines:
   print(str(p))
   print('\n'.join(lines)[:6500])
print('\nScratchpad audit: the preceding scaling calculation only transformed an assumed endpoint witness; it did not construct one or establish existence.')