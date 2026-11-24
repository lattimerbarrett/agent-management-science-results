import sys,itertools
from pathlib import Path
sys.path.insert(0,'workspace')
from agent2_structural_checks import kd_order, subfaces

def check(n,k):
    edges=[sum(1<<i for i in c) for c in itertools.combinations(range(n),2)]
    triples=[sum(1<<i for i in c) for c in itertools.combinations(range(n),3)]
    count=0;graphs=0
    for state in range(1,1<<len(edges)):
        ls=tuple(sorted(e for i,e in enumerate(edges) if state>>i&1))
        if kd_order(ls,k) is None: continue
        graphs+=1
        faces=set().union(*(set(subfaces(e)) for e in ls))
        ts=[f for f in triples if all(s in faces for s in subfaces(f) if s!=f)]
        for extra in range(1<<len(ts)):
            gamma=tuple(sorted({(1<<n)|e for e in ls}|{f for i,f in enumerate(ts) if extra>>i&1}))
            assert kd_order(gamma,k) is not None,(ls,gamma)
            count+=1
    return graphs,count
if __name__=='__main__':
    Path('workspace/agent2_relative_cone_check.py').write_text(Path(__file__).read_text())
    print('All pure vertex-decomposable graph relative cones on 5 labels:',check(5,0))
