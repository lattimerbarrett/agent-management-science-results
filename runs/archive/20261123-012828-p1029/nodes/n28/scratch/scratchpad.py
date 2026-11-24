from pathlib import Path
for fn in ['agent4_reduction_notes.md','agent1_extremal_reduction.md','agent3_completion_audit.md']:
 print('\n### '+fn+'\n'+Path('experiments/e1/'+fn).read_text())
