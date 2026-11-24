from pathlib import Path
for name in ['agent3_completion_audit.md','agent4_reduction_notes.md','agent1_extremal_reduction.md']:
 p=Path('experiments/e1')/name
 print('\n###',name,'\n',p.read_text())
