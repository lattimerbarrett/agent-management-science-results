import sys,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_birth_tree_checks import main
out=main()
Path('workspace/agent4_birth_check_independent.json').write_text(json.dumps(out,indent=2,sort_keys=True))
print('independent agent4 run PASS')