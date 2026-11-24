from pathlib import Path
import json
p=Path('experiments/e4')
for name in ['agent3_s3_global_cases.md','agent2_conditional_edge_closure.md','agent4_reflection_search.py']:
 f=p/name
 if f.exists():print('\nFILE',name,'\n',f.read_text()[:22000])
f=p/'agent4_reflection_edge_cycles.json'
if f.exists():
 a=json.loads(f.read_text()); print('\nCYCLE DATA TYPE',type(a));print(str(a)[:12000])
