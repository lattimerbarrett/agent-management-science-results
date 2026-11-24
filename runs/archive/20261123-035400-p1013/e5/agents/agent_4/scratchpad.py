import sys,time,json
sys.path.insert(0,'workspace')
from agent1_twin_cycle_engine import count_cycles
out=json.load(open('workspace/agent4_multiexception_check.json'))
for m,k in [(80,5)]:
    b=round(.8*m)
    sizes=[m,b,m-b,m,k]
    part=[0,1,1,2,3]
    adj=[[0]*5 for _ in range(5)]
    for i in range(4):
        for j in range(4):adj[i][j]=int(part[i]!=part[j])
    for j in [0,1,4]:adj[4][j]=adj[j][4]=1
    start=time.time()
    ce=count_cycles(sizes,adj)
    cf=count_cycles([m+k,m,m],[[0,1,1],[1,0,1],[1,1,0]])
    ratio=ce/cf;pred=((m+b)/(2*m))**(2*k)
    row=dict(m=m,k=k,ratio=ratio,asymptotic=pred,relative=ratio/pred,seconds=time.time()-start)
    print(row,flush=True);out.append(row)
open('workspace/agent4_multiexception_check.json','w').write(json.dumps(out,indent=2))
import shutil
shutil.copyfile('scratchpad.py','workspace/agent4_multiexception_check.py')
