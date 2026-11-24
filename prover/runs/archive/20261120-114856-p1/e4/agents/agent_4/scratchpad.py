import numpy as np,json
D=json.load(open('workspace/agent4_reflection_edge_cycles.json'))
for i,d in enumerate(D):
 print(i,'geom',d['hf'],'wa',d['wa'],'wb',d['wb'],'mu',d['mu'],'q',d['q'],'r',d['r'],'H',d['H'],'v',d['v'],'mincond',min(d['conds']))
