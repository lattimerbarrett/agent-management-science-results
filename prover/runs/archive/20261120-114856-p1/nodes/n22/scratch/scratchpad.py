from pathlib import Path
for name in ['root_connection_checks_agent2.py','root_barrier_checks_agent2.py','neutral_witness_checks_agent2.py']:
 p=Path('experiments/e1')/name
 print('\n###',name,'\n',p.read_text()[:23000])
