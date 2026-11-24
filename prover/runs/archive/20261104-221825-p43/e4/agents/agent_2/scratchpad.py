from pathlib import Path
import runpy
files=['agent1_lefschetz_check.py','agent2_hamiltonian_check.py','agent3_quantum_check.py','agent4_singleton_obstruction.py']
for filename in files:
    path=Path('workspace')/filename
    print('\nRUNNING',path)
    runpy.run_path(str(path),run_name='__main__')
print('\nAll four agents\' exact algebraic checks passed independently.')