from pathlib import Path
for name in ['agent3_completion_audit.md','agent3_dimension_function_obstruction.py','agent3_qt_ultraproduct_notes.md']:
 p=Path('experiments/e1')/name
 print('\nFILE',name,'\n',p.read_text())
