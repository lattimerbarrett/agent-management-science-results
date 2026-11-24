from itertools import product
from pathlib import Path
import random

def run_checks(seeds=1000, stages=100):
    outcomes=(0,1,2) # 2 denotes infinity
    depth=3
    nodes=[s for k in range(depth+1) for s in product(outcomes,repeat=k)]
    bank={s:set(range(3*i,3*i+3)) for i,s in enumerate(nodes)}
    universe=set().union(*bank.values())
    prefix=lambda s,t:t[:len(s)]==s
    region={s:set().union(*(bank[t] for t in nodes if prefix(s,t))) for s in nodes}
    body={s:bank[s]|set().union(*(region.get(s+(j,),set()) for j in (0,1))) for s in nodes}
    z={s:set().union(*(body[s[:i]] for i,x in enumerate(s) if x==2)) for s in nodes}
    actions=0
    for seed in range(seeds):
        rng=random.Random(seed)
        state={s:[None,0] for s in nodes} # current candidate, next available candidate
        restraints={s:set() for s in nodes}
        D=set()
        def assert_safe():
            assert all(not (P&D) for P in restraints.values())
        def visit(s):
            nonlocal actions
            actions+=1
            cur,nxt=state[s]
            if cur is None and nxt<2 and rng.random()<.45:
                cur=nxt; state[s]=[cur,nxt+1]
            if cur is None:
                # Background only on reset/wait visits; it may delete any body point.
                pool=sorted(body[s])
                if pool:D.add(rng.choice(pool))
                child=2
            elif rng.random()<.25:
                # Reject: release parent candidate and the entire finite child.
                restraints[s].clear()
                for t in nodes:
                    if prefix(s+(cur,),t):restraints[t].clear()
                D.update(region.get(s+(cur,),set()))
                D.add(sorted(bank[s])[cur])
                state[s][0]=None
                pool=sorted(body[s])
                if pool:D.add(rng.choice(pool))
                child=2
            else:
                virtual=z[s]|bank[s]|region.get(s+(cur,),set())
                possible=sorted(universe-D-virtual)
                if possible:
                    # Arbitrary positive witnesses, not chosen to avoid restraints elsewhere.
                    restraints[s].add(rng.choice(possible))
                child=cur
            assert_safe()
            if len(s)<depth: visit(s+(child,))
        for stage in range(stages):visit(())
    return {'seeds':seeds,'stages_per_seed':stages,'audited_node_actions':actions}

if __name__=='__main__':
    print(run_checks())
