from pathlib import Path
for name in ['agent3_arc_checks.py','agent2_local_germ_checks.py']:
 p=Path('experiments/e1')/name
 print('\nFILE',p,'\n',p.read_text()[:22000])
