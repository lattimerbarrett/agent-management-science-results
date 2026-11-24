from pathlib import Path
source = Path('workspace/agent1_complete_checks.py').read_text()
# Retain all mathematical checks and printing, omit writes to protected workspace.
source = source.split("with open('workspace/agent1_complete_checks.json'")[0]
exec(compile(source, 'workspace/agent1_complete_checks.py', 'exec'))
