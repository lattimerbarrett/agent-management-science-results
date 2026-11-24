"""Finite exhaustive checks of birth-only oracle-tree realization.
No claim to decide an infinite arithmetical property is made.
Each of 9072 executions uses a monotone 4-bit oracle approximation,
local permanently deleted column sets, global irreversible emissions,
and finite or infinite symbolic hypergraph requirements.
"""
from itertools import product
import json

def execute(times, seed, stages=70):
    tree={}; D=set(); births=[]; neg=[]
    def oracle(t,s): return times[t] is not None and times[t]<=s
    def actual(t): return times[t] is not None
    # Nodes have paths in {0,1,2}^{<omega}; 2 is a nonquery continuation.
    def follow(s,truth=False):
        p=()
        while p in tree:
            v=tree[p]
            bit=actual(v['q']) if truth else oracle(v['q'],s)
            p=p+(int(bit) if v['query'] else 2,)
        return p
    def incoming(p):
        if not p:return frozenset()
        par=tree[p[:-1]]; z=set(par['out'])
        if par['query'] and p[-1]==1 and par['q']%2==0:
            z.add(0) # toy oracle-dependent diagonal action
        return frozenset(z)
    for s in range(stages):
        p=follow(s); n=len(p); z=incoming(p)
        before=set(D)
        D.update((i,k) for i in range(min(3,n+1)) if i not in z for k in range(n+1))
        emitted=D-before
        out=set(z); query=n%3==0; q=(n//3)%4
        edge=None; positive=False
        # Column 2 is always protected; it supplies a true-1 growth test.
        I={2}-out
        if not query:
            C={i for i in range(3) if (seed+1)&(1<<i)}
            if not C:C={0}
            if n%2:
                # E_C has edge {(i,k):i in C} for every k in omega.
                positive=bool(C&I)
                if not positive:
                    k=1+max([b for a,b in D if a in C]+[-1])
                    edge=frozenset((i,k) for i in C)
            else:
                # A finite hypergraph tests covers using finite P as well.
                edges=[frozenset({(i,(seed+j)%4) for i in C}) for j in range(2)]
                positive=all(any(i in I or (i,k) in D for i,k in e) for e in edges)
                if not positive:edge=next(e for e in edges if all(i not in I and (i,k) not in D for i,k in e))
            if edge is not None:
                assert not (edge&D)
                assert all(i not in I for i,k in edge)
                out.update(i for i,k in edge)
                neg.append((p,edge,s))
        tree[p]={'in':z,'out':frozenset(out),'q':q,'query':query,'stage':s,'emitted':emitted}
        births.append(p)
    # Determine all created nodes on the actual-oracle history.
    p=(); true=[]
    while p in tree:
        true.append(p);v=tree[p]
        p=p+(int(actual(v['q'])) if v['query'] else 2,)
    true=set(true)
    cones=negative=zero=emission=0
    for p in true:
        v=tree[p]; s=v['stage']
        # Once a true node is born every future birth is its descendant.
        for r in births[s+1:]:
            assert r[:len(p)]==p
            cones+=1
        # Every incoming true-zero column remains zero in all future nodes.
        for i in v['in']:
            for r in births[s+1:]:
                assert i in tree[r]['in']
                assert all(a!=i for a,k in tree[r]['emitted'])
                zero+=1
        # Every point scheduled at each true-1 birth really was emitted.
        n=len(p)
        for i in range(min(3,n+1)):
            if i not in v['in']:
                assert all((i,k) in D for k in range(n+1))
                emission+=1
    for p,e,s in neg:
        if p in true:
            assert not e&D
            negative+=1
    return len(tree),cones,negative,zero,emission

def main():
    totals=[0]*5; cases=0
    for times in product([None,0,1,2,3,4],repeat=4):
        for seed in range(7):
            a=execute(times,seed)
            totals=[x+y for x,y in zip(totals,a)];cases+=1
    out=dict(zip(['nodes','true_cone_checks','preserved_negative_edges','zero_column_checks','true_one_emission_checks'],totals))
    out['executions']=cases
    print(json.dumps(out,sort_keys=True))
    return out
if __name__=='__main__':
    result=main()
    from pathlib import Path
    Path('workspace/agent2_birth_tree_checks.json').write_text(json.dumps(result,indent=2,sort_keys=True))
