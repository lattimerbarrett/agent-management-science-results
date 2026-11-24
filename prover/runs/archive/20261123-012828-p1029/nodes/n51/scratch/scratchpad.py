from pathlib import Path
for p in ['experiments/e1/agent1_extremal_reduction.md','experiments/e1/agent4_reduction_notes.md','experiments/e1/agent3_completion_audit.md']:
 print('\n###',p,'\n',Path(p).read_text()[:24000])
print('\nE2 FILES')
for p in Path('experiments/e2').rglob('*'):
 if p.is_file(): print(p)
