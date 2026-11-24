from pathlib import Path
for name in ['agent4_reduction_notes.md','agent3_completion_audit.md','agent1_extremal_reduction.md']:
    p=Path('experiments/e1')/name
    print('\n###',name,'###\n')
    print(p.read_text()[:26000])
