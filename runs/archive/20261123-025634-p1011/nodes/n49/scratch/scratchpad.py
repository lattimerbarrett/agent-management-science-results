from pathlib import Path
base=Path('experiments/e3')
for p in sorted(base.glob('*.md')):
    if any(s in p.name for s in ['sharp','critical','estimate','simple']):
        print('\n###',p.name,'###\n',p.read_text()[:26000])
