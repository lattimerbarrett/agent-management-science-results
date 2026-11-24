from itertools import combinations
from pathlib import Path
import z3,json,time

def solve(n,d=3,timeout=60000):
    Fs=[sum(1<<v for v in c) for c in combinations(range(n),d+1)]
    m=len(Fs); ranks=[z3.Int('r%d'%i) for i in range(m)]
    sel=[r>=0 for r in ranks]
    solver=z3.Solver();solver.set(timeout=timeout)
    for r in ranks:solver.add(r>=-1,r<m)
    solver.add(ranks[0]==0)
    solver.add(z3.Sum([z3.If(x,1,0) for x in sel])<m)
    # Selected facets have distinct ranks, unused ranks can all be -1.
    for i in range(m):
        for j in range(i):solver.add(z3.Or(z3.Not(sel[i]),z3.Not(sel[j]),ranks[i]!=ranks[j]))
    faces=[sum(1<<v for v in c) for s in (1,2,3) for c in combinations(range(n),s)]
    containing={H:[j for j,F in enumerate(Fs) if F&H==H] for H in faces}
    present={H:z3.Or([sel[j] for j in containing[H]]) for H in faces}
    for v in range(n):solver.add(present[1<<v])
    for i,F in enumerate(Fs):
        low=[H for H in faces if H&F==H and H.bit_count()<d]
        ridges=[H for H in faces if H&F==H and H.bit_count()==d]
        before={H:z3.Or([z3.And(sel[j],ranks[j]<ranks[i]) for j in containing[H] if j!=i]) for H in low+ridges}
        clauses=[z3.Or([before[R] for R in ridges])]
        for H in low:
            clauses.append(z3.Implies(before[H],z3.Or([before[R] for R in ridges if R&H==H])))
        solver.add(z3.Implies(z3.And(sel[i],i!=0),z3.And(clauses)))
        # Nonselected F must have a maximal common face below ridge dimension.
        obstruction=[z3.And(present[H],z3.Not(z3.Or([present[R] for R in ridges if R&H==H]))) for H in low]
        solver.add(z3.Implies(z3.Not(sel[i]),z3.Or(obstruction)))
    print('Start',n,'facets',m,'assertions',len(solver.assertions()),flush=True)
    t=time.time();out=solver.check();print('Result',n,out,'seconds',time.time()-t,flush=True)
    if out==z3.sat:
        model=solver.model();order=sorted([(model[r].as_long(),i) for i,r in enumerate(ranks) if model[r].as_long()>=0])
        result={'n':n,'d':d,'facets':Fs,'order':[i for _,i in order]}
        Path('workspace/agent3_z3_witness.json').write_text(json.dumps(result));print(result,flush=True)
    return out

solve(8)
solve(9)
