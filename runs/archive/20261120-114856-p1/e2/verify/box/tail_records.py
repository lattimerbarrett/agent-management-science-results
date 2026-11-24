from pathlib import Path
for p in sorted(Path('/mnt').glob('nothing')): pass
for name in ['agent_1','agent_2','agent_3','agent_4']:
 p=Path('../record/transcripts')/(name+'.md')
 if not p.exists(): p=Path('record/transcripts')/(name+'.md')
 print('\n===',p,'===')
 try:
  s=p.read_text(); ls=s.splitlines(); print('TOTAL LINES',len(ls)); print('\n'.join(f'{i+1}: {l}' for i,l in list(enumerate(ls))[-80:]))
 except Exception as e: print(e)
