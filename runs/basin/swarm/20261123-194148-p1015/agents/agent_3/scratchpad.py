from pathlib import Path
import importlib.util,json
p=Path('workspace/agent2_birth_tree_checks.py')
spec=importlib.util.spec_from_file_location('birth_check',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
result=m.main()
expected=json.loads(Path('workspace/agent2_birth_tree_checks.json').read_text())
assert result==expected,(result,expected)
Path('workspace/agent3_independent_birth_check.json').write_text(json.dumps({'independent_rerun':result,'matches_agent2':True},indent=2))
print('PASS independent execution and exact agreement')