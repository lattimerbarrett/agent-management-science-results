from pathlib import Path
root=Path('experiments')
for name in ['e1/workspace/agent3_completion_audit.md','e1/workspace/agent4_reduction_notes.md']:
 p=root/name
 print('\nFILE:', p)
 if p.exists():
  text=p.read_text()
  print(text[:22000])
 else:
  print('Not present at this path')