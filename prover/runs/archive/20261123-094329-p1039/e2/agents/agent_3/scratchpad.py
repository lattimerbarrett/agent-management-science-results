from pathlib import Path
import runpy
files=sorted(Path('workspace').glob('*.py'))
for p in files:
    print('\nEXECUTING',p,flush=True)
    runpy.run_path(str(p),run_name='__main__')
print('\nExecuted',len(files),'standalone checker scripts successfully. These check formulas only, not the missing Oka existence claims.')
