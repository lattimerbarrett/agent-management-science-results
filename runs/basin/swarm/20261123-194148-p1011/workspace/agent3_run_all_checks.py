"""Run the algebraic certificates used in the dimension threshold proof.
Analytic PDE estimates are mathematical arguments, not numerical assertions.
Run this file from the directory containing workspace/.
"""
from pathlib import Path
checks=[
 'agent4_shape_checks.py',
 'agent1_all_exact_spd.py',
 'agent3_finite_n.py',
 'agent3_all_n33.py',
 'agent3_transcert.py',
 'agent3_transall.py',
 'agent3_flat_base.py',
 'agent3_pohozaev_identity.py',
 'agent3_mass_rim.py',
 'agent1_linear_stress_rim.py',
 'agent2_dilation_rim.py',
]
for file in checks:
    path=Path('workspace')/file
    print('\n===== '+file+' =====',flush=True)
    namespace={'__name__':'__main__','__file__':str(path)}
    exec(compile(path.read_text(),str(path),'exec'),namespace)
print('ALL symbolic, exact-rational, and outward-interval checks passed.')
