from itertools import combinations
from pathlib import Path
import z3,time,sys,json
sys.path.insert(0,'workspace');from a3_fastkd import kd
n=8
F=[sum(1<<v for v in cc) for cc in combinations(range(n),4)];X=[z3.Bool('x%d'%i) for i in range(len(F))]
faces=[sum(1<<v for v in cc) for k in (1,2) for cc in combinations(range(n),k)]
ridges=sorted({g^(1<<v) for g in F for v in range(n) if g>>v&1})
B={h:z3.Or([X[j] for j,g in enumerate(F) if g&h==h]) for h in ridges}
E={h:z3.Or([X[j] for j,g in enumerate(F) if g&h==h]) for h in faces if h.bit_count()==2}
s=z3.Solver();s.set(timeout=100000)
def purity(sigma,added=None):
    clauses=[];cont=[]
    for j,g in enumerate(F):
        if g&sigma!=sigma:continue
        present=z3.BoolVal(True) if added==j else X[j];cont.append(present)
        for v in range(n):
            if not sigma>>v&1:continue
            ridge=g^(1<<v)
            # Support must be in ANOTHER facet, not g.
            support=z3.BoolVal(True) if added is not None and added!=j and F[added]&ridge==ridge else z3.Or([X[k] for k,h in enumerate(F) if k!=j and h&ridge==ridge])
            clauses.append(z3.Or(z3.Not(present),support))
    return z3.And(z3.Or(cont),*clauses)
S={h:purity(h) for h in faces}
s.add(S[3])
s.add(z3.Or([z3.Not(x) for x in X]))
# Fixed edge01 must have connected link; fix a containing facet0123 WLOG.
s.add(X[F.index(15)])
levels={v:z3.Int('lev%d'%v) for v in range(2,n)}
s.add(levels[2]==0)
for v in range(3,n):
    s.add(levels[v]>=1,levels[v]<=n)
    incident=[];earlier=[]
    for w in range(2,n):
        if w==v:continue
        e=X[F.index(3|(1<<v)|(1<<w))]
        incident.append(e);earlier.append(z3.And(e,levels[w]<levels[v]))
    s.add(z3.Implies(z3.Or(incident),z3.Or(earlier)))

for v in range(n):s.add(z3.Or([X[j] for j,g in enumerate(F) if g>>v&1]))
for i,g in enumerate(F):
    vs=[v for v in range(n) if g>>v&1];boundary=[B[g^(1<<v)] for v in vs]
    legal=z3.Or(z3.PbGe([(a,1) for a in boundary],3),*[z3.And(boundary[a],boundary[b],z3.Not(E[(1<<vs[a])|(1<<vs[b])])) for a,b in combinations(range(4),2)])
    for sigma in faces:
        s.add(z3.Implies(z3.And(z3.Not(X[i]),legal),z3.Not(purity(sigma,i))))
# Facet-ridge adjacency must be connected for a shellable input.
fl=[z3.Int('facetlevel%d'%i) for i in range(len(F))]
s.add(fl[0]==0)
for i,g in enumerate(F):
    if i==0:continue
    s.add(fl[i]>=1,fl[i]<=len(F))
    s.add(z3.Implies(X[i],z3.Or([z3.And(X[j],fl[j]<fl[i]) for j,h in enumerate(F) if j!=i and (h&g).bit_count()==3])))
print('encoded',len(s.assertions()),flush=True);start=time.time()
for it in range(10000):
    res=s.check();print('result',res,'time',time.time()-start,flush=True) if it%100==0 or res!=z3.sat else None
    if res!=z3.sat:break
    m=s.model();fs=tuple(g for j,g in enumerate(F) if z3.is_true(m[X[j]]))
    print('facets',len(fs),'kd?',kd(fs,1),flush=True) if it%100==0 else None
    if kd(fs,1):
        assert len(fs)<len(F)
        bad=[g for g in F if g not in fs and kd(tuple(sorted(fs+(g,))),1)]
        assert not bad,bad
        print('TRUE OBSTRUCTION',fs,flush=True);Path('workspace/agent1_purity_trap.json').write_text(json.dumps(fs));break
    s.add(z3.Or([z3.Not(x) if F[j] in fs else x for j,x in enumerate(X)]))
    if time.time()-start>100:break

