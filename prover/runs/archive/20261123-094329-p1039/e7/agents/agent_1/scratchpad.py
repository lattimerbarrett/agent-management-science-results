from pathlib import Path
files=sorted(Path('workspace').glob('*checks.py'))
for p in files:
 print('\n===== CHECKING',p.name,'=====')
 exec(compile(p.read_text(),str(p),'exec'),{'__name__':'__main__'})
print('\nALL',len(files),'CHECK SCRIPTS EXECUTED SUCCESSFULLY.')
