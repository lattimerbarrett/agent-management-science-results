import sys,time,json
from pathlib import Path
sys.path.insert(0,'workspace')
from agent1_twin_cycle_engine import count_cycles
out=[]
for m in [5,10,20,40,80]:
 b=4*m//5
 sizes=[m,b,m-b,m,2];part=[0,1,1,2,3]
 adj=[[int(i<4 and j<4 and part[i]!=part[j]) for j in range(5)] for i in range(5)]
 for i in [0,1]:adj[i][4]=adj[4][i]=1
 adj[4][4]=1
 t=time.time();actual=count_cycles(sizes,adj)
 clone=count_cycles([m,m,m+2],[[0,1,1],[1,0,1],[1,1,0]])
 row={'m':m,'ratio':actual/clone,'prediction':(.9)**4,'seconds':time.time()-t}
 print(row,flush=True);out.append(row)
Path('workspace/agent3_two_exception_checks.json').write_text(json.dumps(out,indent=2))
