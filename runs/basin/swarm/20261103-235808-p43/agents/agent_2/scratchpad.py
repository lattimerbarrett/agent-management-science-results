from pathlib import Path
code=Path('workspace/agent2_planar_merger.py').read_text()
assert 'write_text' not in code and 'scratchpad' not in code
Path('workspace/agent2_planar_checks_final.py').write_text(code)
exec(compile(code,'workspace/agent2_planar_checks_final.py','exec'))