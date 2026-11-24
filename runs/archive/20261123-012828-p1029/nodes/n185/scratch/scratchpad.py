from pathlib import Path
for name in ['experiments/e1/agent3_completion_audit.md','experiments/e1/agent4_reduction_notes.md','experiments/e1/agent3_qt_ultraproduct_notes.md','experiments/e1/agent1_extremal_reduction.md']:
 print('\nFILE',name,'\n',Path(name).read_text())