from pathlib import Path
p=Path('experiments/e2')
for name in ['agent4_lshape.py','agent4_n7_exact.py','agent4_rationalized_mp.py','agent2_mixed_billiards.py','agent4_seedpassing_mp.py']:
 f=p/name
 if f.exists(): print('\nFILE',name,'\n',f.read_text()[-8500:])
print('\nOTHER RELEVANT NAMES\n', '\n'.join(f.name for f in p.iterdir() if any(s in f.name for s in ['n7','n8','lshape','junction'])))
