from itertools import combinations
import z3,time,pickle
T=5; L=5
cores=[set(range(i*L,(i+1)*L)) for i in range(T)]
U=set(range(T*L))
A={L,2*L}
E=[]; R=[]; color=[]
for i in range(T):
    rr=[{x} for x in A] if i==0 else map(set,combinations(U-cores[i],2))
    for r in rr:
        e=cores[i]|r
        if i and any(not(e&(cores[0]|{x})) for x in A):continue
        E.append(e);R.append(r);color.append(i)
s=z3.Solver();s.set(timeout=10000)
b=[z3.Bool('b%d'%i) for i in range(len(E))]
for i in range(T):s.add(z3.Or([b[j] for j in range(len(E)) if color[j]==i]))
s.add(b[0],b[1])
for i in range(len(E)):
    for j in range(i):
        if color[i]!=color[j] and not(E[i]&E[j]):s.add(z3.Or(z3.Not(b[i]),z3.Not(b[j])))
print('edges',len(E),flush=True)
start=time.time()
for C0 in combinations(U,T-1):
    C=set(C0)
    s.add(z3.Or([b[j] for j,e in enumerate(E) if not(e&C)]))
print('all cover constraints added',time.time()-start,flush=True)
s.set(timeout=240000)
for it in range(1000):
    ans=s.check()
    if ans!=z3.sat:
        print(ans,'iteration',it,flush=True);break
    m=s.model();sel=[i for i in range(len(E)) if z3.is_true(m.eval(b[i]))]
    cs=z3.Solver();v=[z3.Bool('v%d'%j) for j in U]
    cs.add(z3.PbLe([(x,1) for x in v],T-1))
    for j in sel:cs.add(z3.Or([v[x] for x in E[j]]))
    if cs.check()==z3.unsat:
        print('FOUND',[(color[j],R[j]) for j in sel],flush=True)
        pickle.dump((cores,E,R,color,sel),open('found.pkl','wb'));break
    cm=cs.model();C={x for x in U if z3.is_true(cm.eval(v[x]))}
    s.add(z3.Or([b[j] for j,e in enumerate(E) if not(e&C)]))
    if it%100==0:print(it,'sel',len(sel),'C',C,'time',round(time.time()-start,2),flush=True)
else: print('iteration limit')
