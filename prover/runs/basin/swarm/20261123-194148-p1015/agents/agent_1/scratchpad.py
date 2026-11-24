import importlib.util,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('birth_checks','workspace/agent2_birth_tree_checks.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
r=m.main()
Path('workspace/agent1_birth_check_independent.json').write_text(json.dumps(r,indent=2,sort_keys=True))