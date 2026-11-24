from pathlib import Path
p=Path('workspace/agent4_checks.py')
assert p.is_file()
exec(compile(p.read_text(), str(p), 'exec'))
