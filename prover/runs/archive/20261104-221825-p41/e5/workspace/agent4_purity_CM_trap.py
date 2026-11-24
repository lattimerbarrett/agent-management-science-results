from itertools import combinations
from pathlib import Path
import z3,time,sys,json
sys.path.insert(0,'workspace');from a3_fastkd import kd
helper=Path('workspace/agent4_terminal_CM_guarded.py').read_text()
exec(helper[:helper.index('n=12')])
n=9
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
s.add(S[3]);s.add(*[z3.Not(v) for h,v in S.items() if h!=3])
for v in range(n):s.add(z3.Or([X[j] for j,g in enumerate(F) if g>>v&1]))
for i,g in enumerate(F):
    vs=[v for v in range(n) if g>>v&1];boundary=[B[g^(1<<v)] for v in vs]
    legal=z3.Or(z3.PbGe([(a,1) for a in boundary],3),*[z3.And(boundary[a],boundary[b],z3.Not(E[(1<<vs[a])|(1<<vs[b])])) for a,b in combinations(range(4),2)])
    for sigma in faces:
        s.add(z3.Implies(z3.And(z3.Not(X[i]),legal),z3.Not(purity(sigma,i))))
s.add(z3.Or([z3.Not(x) for x in X]))
print('encoded',len(s.assertions()),flush=True);start=time.time()
for it in range(50000):
    res=s.check();
    if it%100==0 or res!=z3.sat:print('result',it,res,'time',time.time()-start,flush=True)
    if res!=z3.sat:break
    m=s.model();fs=tuple(g for j,g in enumerate(F) if z3.is_true(m[X[j]]))
    C=faces_from_facets(fs);cmcuts=[]
    present={0:z3.BoolVal(True),**{1<<v:z3.BoolVal(True) for v in range(n)},**B,**E}
    for tau in C:
        if tau.bit_count()>2:continue
        L={g^tau for g in C if g&tau==tau}
        for i in range(3-tau.bit_count()):
            witness=nonzero_homology_cochain(L,i)
            if witness is None:continue
            support,cycle=witness;possible=[]
            for j,g in enumerate(F):
                if g&tau!=tau:continue
                h=g^tau;vv=[v for v in range(n) if h>>v&1]
                if any(sum(1 for a in support if a&sub==a)%2 for sub in [sum(1<<v for v in cc) for cc in combinations(vv,i+2)]):possible.append(j)
            assert possible and not any(F[j] in fs for j in possible)
            cmcuts.append(z3.Or([z3.Not(present[tau|g]) for g in cycle]+[X[j] for j in possible]))
    if cmcuts:
        s.add(*cmcuts)
        if time.time()-start>100:break
        continue
    print('CM candidate',len(fs),'facets',flush=True)
    if kd(fs,1):
        bad=[g for g in F if g not in fs and kd(tuple(sorted(fs+(g,))),1)]
        assert any(g not in fs for g in F)
        assert not bad,bad
        print('TRUE OBSTRUCTION',fs,flush=True);Path('workspace/a4_purity_trap.json').write_text(json.dumps(fs));break
    s.add(z3.Or([z3.Not(x) if F[j] in fs else x for j,x in enumerate(X)]))
    if time.time()-start>100:break

