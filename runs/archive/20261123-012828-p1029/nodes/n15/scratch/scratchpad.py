from pathlib import Path
for folder in ('experiments/e1','experiments/e2'):
    files=list(Path(folder).rglob('*'))
    print(folder, 'files',len(files))
    for p in files[:25]: print(p)
