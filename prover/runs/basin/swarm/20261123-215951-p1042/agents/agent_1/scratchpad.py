from pathlib import Path
p=Path('workspace/a1_standalone.py');s=p.read_text().replace('i=min(units,key=lambda i:len(R[i]))','i=min(units,key=lambda i:(len(R[i]),i))');p.write_text(s)
import sys;sys.path.insert(0,'workspace')
from a1_standalone import invariant_data
for m in range(7,11):print(m,invariant_data(m),flush=True)
