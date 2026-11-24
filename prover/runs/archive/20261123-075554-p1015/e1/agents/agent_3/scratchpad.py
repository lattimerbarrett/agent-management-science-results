import importlib.util
from pathlib import Path
files=['agent3_upper_checks.py','agent3_tree_checks.py','agent2_order_checks.py','agent2_tree_checks.py','agent4_tree_checks.py']
for fn in files:
    p=Path('workspace')/fn
    spec=importlib.util.spec_from_file_location(fn[:-3],p)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    print(fn, m.run_checks())
