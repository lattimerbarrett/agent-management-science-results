from pathlib import Path
for experiment in ('e1','e2','e3'):
 root=Path('experiments')/experiment
 print('\nEXPERIMENT',experiment)
 if root.exists():
  for p in root.iterdir():
   if p.is_file() and p.suffix in ('.md','.json'):
    print(p.name)
p=Path('experiments/e1/agent4_reduction_notes.md')
text=p.read_text()
print('\nINTERPOLATION AND STATUS RECORD\n',text)
