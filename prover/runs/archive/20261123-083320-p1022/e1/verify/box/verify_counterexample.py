from pathlib import Path
source = Path('workspace/agent4_counterexample_checks.py').read_text()
source = source.split("Path('workspace/agent4_counterexample_checks.json')")[0]
exec(compile(source, 'workspace/agent4_counterexample_checks.py', 'exec'))
print(json.dumps(results, indent=2))
