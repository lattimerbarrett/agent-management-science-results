from pathlib import Path
print('\n'.join(str(p) for p in Path('workspace').glob('*matching*')))
print('\n'.join(str(p) for p in Path('workspace').glob('*gem*')))