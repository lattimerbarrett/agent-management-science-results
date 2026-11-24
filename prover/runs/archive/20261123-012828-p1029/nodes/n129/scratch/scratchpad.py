from pathlib import Path
print('cwd entries:',[p.name for p in Path('.').iterdir()])
for p in Path('experiments').rglob('*'):
    if p.name in ('agent3_qt_ultraproduct_notes.md','agent1_extremal_reduction.md','agent4_reduction_notes.md'):
        print('\n---',p,'---\n',p.read_text()[:24000])
