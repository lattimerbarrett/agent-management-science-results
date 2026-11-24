from pathlib import Path
for name in ['agent4_reduction_notes.md','agent3_completion_audit.md']:
    p=Path('experiments/e1')/name
    print('\n###',name)
    print(p.read_text()[:24000] if p.exists() else 'not present')
