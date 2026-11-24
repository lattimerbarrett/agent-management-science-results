from pathlib import Path
p=Path('experiments/e1/workspace')
print('Workspace available:', p.exists())
if p.exists():
    print('\n'.join(str(x) for x in p.glob('*conflict*')))
    for x in p.glob('*conflict*.md'):
        print(x.read_text()[:18000])
else:
    print('No independent certificate files available at the supplied relative path.')
