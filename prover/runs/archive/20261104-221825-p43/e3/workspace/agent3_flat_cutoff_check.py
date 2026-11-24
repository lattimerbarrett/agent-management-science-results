from pathlib import Path
p=Path('workspace/agent2_verify_completed_components.py')
p.write_text('''"""Run exact/sound interval checks used by the completed analytic proof.
This verifies finite algebra/inequalities, not the analytic theorems themselves.
"""
import runpy
from pathlib import Path
root=Path(__file__).resolve().parent
files=[
 'agent2_lower_checks.py',
 'agent2_radial_bound.py',
 'agent2_collapse_axes_check.py',
 'agent3_flat_cutoff_check.py',
 'agent3_global_geometry_checks.py',
 'agent4_ellipsoid_check.py',
]
for f in files:
 print('\\n===',f,'===')
 runpy.run_path(str(root/f),run_name='__main__')
print('\\nAll selected exact/interval proof-component checks passed.')
''')
import runpy
runpy.run_path(str(p),run_name='__main__')