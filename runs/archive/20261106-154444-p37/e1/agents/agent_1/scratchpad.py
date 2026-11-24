from pathlib import Path
print(Path('workspace/dedekind_upper_check.py').read_text())
exec(compile(Path('workspace/dedekind_upper_check.py').read_text(), 'workspace/dedekind_upper_check.py', 'exec'))