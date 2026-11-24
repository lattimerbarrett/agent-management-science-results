from pathlib import Path
import runpy
names=['workspace/lower25_agent4.py','workspace/agent3_fz25_exact.py']
for name in names:
 before=Path(name).read_bytes()
 runpy.run_path(name,run_name='__main__')
 assert Path(name).read_bytes()==before
print('Both primary certificate programs reproduced; source files unchanged.')