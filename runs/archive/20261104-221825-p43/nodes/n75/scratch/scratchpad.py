from pathlib import Path
for f in ['experiments/e1/agent3_arc_checks.py','experiments/e1/agent2_local_germ_checks.py','experiments/e1/slow_hamiltonian_checks.py']:
 print('\n###',f,'\n',Path(f).read_text())
