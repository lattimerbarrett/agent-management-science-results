from pathlib import Path
p=Path('workspace/agent4_shift_checks.py')
s=p.read_text()
s=s[:s.index("    os.makedirs('workspace',exist_ok=True)")]
s=s.replace('results=[check(6,4),check(7,4),check(8,6)]','results=[check(5,4),check(6,4),check(7,4),check(8,6)]')
p.write_text(s)
import runpy
runpy.run_path(str(p),run_name='__main__')
