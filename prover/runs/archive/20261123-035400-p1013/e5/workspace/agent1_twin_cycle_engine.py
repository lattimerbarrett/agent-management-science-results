from collections import defaultdict
from math import prod
from pathlib import Path
import json,time

def count_cycles(sizes,adj):
    sizes=tuple(sizes);q=len(sizes);total=0
    for start,ns in enumerate(sizes):
        if not ns:continue
        init=[0]*q;init[start]=1
        front={(tuple(init),start):1};length=1;buckets=defaultdict(int)
        nbr={i:[j for j in range(start,q) if adj[i][j]] for i in range(start,q)}
        while front:
            nxt=defaultdict(int)
            for (used,last),ways in front.items():
                if length>=3 and adj[last][start]:buckets[used[start]]+=ways
                for j in nbr[last]:
                    left=sizes[j]-used[j]
                    if left:
                        u=list(used);u[j]+=1
                        nxt[tuple(u),j]+=ways*left
            front=nxt;length+=1
        for k,w in buckets.items():
            assert (ns*w)%(2*k)==0,(sizes,start,k,w)
            total+=ns*w//(2*k)
    return total

def model_ext(m):
    # A ordinary, B ordinary, two A triangles, two B triangles.
    sz=[m+1-6,m-6,3,3,3,3];part=[0,1,0,0,1,1];q=len(sz)
    adj=[[int(part[i]!=part[j] or (i==j and i>=2)) for j in range(q)] for i in range(q)]
    return sz,adj

def model_q(m):
    # Q=subdivided K33: 0,3,6 singletons; left other2, right other2.
    sz=[m+1-7,m,1,1,1,2,2];q=len(sz)
    adj=[[0]*q for _ in range(q)]
    for i in [0,2,3,4,5,6]:adj[1][i]=adj[i][1]=1
    for i,j in [(2,4),(4,3),(2,6),(5,3),(5,6)]:adj[i][j]=adj[j][i]=1
    return sz,adj

if __name__=='__main__':
    for a,b,c in [(2,2,1),(3,2,3),(3,3,15)]:
        assert count_cycles([a,b],[[0,1],[1,0]])==c
    out=[]
    for m in [6,8,10,15,20,30,50]:
        t=time.time();ce=count_cycles(*model_ext(m));cq=count_cycles(*model_q(m))
        z={'n':2*m+1,'Q_cycles':str(cq),'ext_cycles':str(ce),'Q_gt_ext':cq>ce,'ratio':float(cq/ce),'seconds':time.time()-t}
        out.append(z);print({k:v for k,v in z.items() if k not in ['Q_cycles','ext_cycles']},flush=True)
    Path('workspace/agent1_r2_cycle_comparison.json').write_text(json.dumps(out,indent=2))
    Path('workspace/agent1_twin_cycle_engine.py').write_text(Path(__file__).read_text())
