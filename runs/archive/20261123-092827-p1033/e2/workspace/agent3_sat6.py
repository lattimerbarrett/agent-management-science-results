import itertools, time, json, os
import z3
open('workspace/agent3_sat6.py','w').write(open(__file__).read())
T=6; D=2; S=4; N=T*S; K=S+D
cores=[sum(1<<(i*S+j) for j in range(S)) for i in range(T)]
modes=[]; byowner=[]
for i in range(T):
    inds=[]
    avail=[p for p in range(N) if not (cores[i]>>p)&1]
    for pair in itertools.combinations(avail,D):
        r=sum(1<<p for p in pair)
        inds.append(len(modes)); modes.append((i,r,cores[i]|r))
    byowner.append(inds)
xs=[z3.Bool('e%d'%i) for i in range(len(modes))]
sol=z3.Solver(); sol.set(timeout=60000)
npair=0
for a,(i,r,e) in enumerate(modes):
    for b in range(a):
        j,s,f=modes[b]
        if i!=j and not e&f:
            sol.add(z3.Or(z3.Not(xs[a]),z3.Not(xs[b]))); npair+=1
print('modes',len(modes),'incompat',npair,flush=True)
# Full uniform covering number K implies each vertex of any edge has a private witness.
for a,(i,r,e) in enumerate(modes):
    for v in range(N):
        if (e>>v)&1:
            witnesses=[xs[b] for b,(_,_,f) in enumerate(modes) if e&f==1<<v]
            sol.add(z3.Implies(xs[a],z3.Or(witnesses)))
# Symmetry branch: seek a mode touching two distinct foreign cores.
fixed=next(q for q,(i,r,e) in enumerate(modes) if i==0 and r==(1<<4 | 1<<8))
sol.add(xs[fixed])
print('witness clauses added',flush=True)
# Iterative counterexample-guided covers, greedy model initial all groups nonempty
for inds in byowner: sol.add(z3.Or([xs[q] for q in inds]))
start=time.time(); result='unknown'; covers=0
for step in range(20):
    st=sol.check()
    print('step',step,st,'sec',time.time()-start,flush=True)
    if st!=z3.sat: result=str(st); break
    model=sol.model(); selected=[q for q,x in enumerate(xs) if z3.is_true(model.eval(x))]
    es=[modes[q][2] for q in selected]
    found=[]
    for C in itertools.combinations(range(N),T-1):
        mask=sum(1<<p for p in C)
        if all(mask&e for e in es):
            found.append(mask)
            if len(found)>=100: break
    if not found:
        result='verified'; print('SUCCESS',selected,flush=True)
        json.dump({'modes':[modes[q] for q in selected],'cores':cores,'K':K},open('workspace/agent3_sat6.json','w'));break
    for mask in found:
        sol.add(z3.Or([xs[q] for q,(_,_,e) in enumerate(modes) if not mask&e])); covers+=1
print('result',result,'covers',covers,flush=True)
