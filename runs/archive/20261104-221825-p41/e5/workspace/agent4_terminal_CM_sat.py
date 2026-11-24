from itertools import combinations
from pathlib import Path
import z3,time,sys,json
sys.path.insert(0,'workspace');from a3_fastkd import kd

def nullspace(rows,q):
    basis={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j not in basis:basis[j]=x;break
            x^=basis[j]
    result=[]
    for j in range(q):
        if j in basis:continue
        v=1<<j
        for p in sorted(basis):
            if (basis[p]&v).bit_count()%2:v^=1<<p
        assert all((x&v).bit_count()%2==0 for x in rows)
        result.append(v)
    return result

def solve(rows,q):
    basis={}
    for x,b in rows:
        while x:
            j=x.bit_length()-1
            if j not in basis:basis[j]=(x,b);break
            y,c=basis[j];x^=y;b^=c
        else:
            if b:raise ValueError('inconsistent')
    v=0
    for j,(x,b) in sorted(basis.items()):
        if ((x&v).bit_count()%2)!=b:v^=1<<j
    assert all((x&v).bit_count()%2==b for x,b in rows)
    return v

def nonzero_homology_cochain(linkfaces,i):
    cells=sorted(g for g in linkfaces if g.bit_count()==i+1); idx={g:j for j,g in enumerate(cells)}
    if not cells:return None
    lower=[g for g in linkfaces if g.bit_count()==i]
    rows=[sum(1<<j for j,g in enumerate(cells) if g&h==h) for h in lower]
    cycles=nullspace(rows,len(cells))
    boundaries=[sum(1<<j for j,g in enumerate(cells) if g&h==g) for h in linkfaces if h.bit_count()==i+2]
    basis={}
    for x in boundaries:
        while x:
            j=x.bit_length()-1
            if j not in basis:basis[j]=x;break
            x^=basis[j]
    for z in cycles:
        r=z
        while r:
            j=r.bit_length()-1
            if j not in basis:
                u=solve([(x,0) for x in boundaries]+[(z,1)],len(cells))
                return [g for j,g in enumerate(cells) if u>>j&1]
            r^=basis[j]
    return None

def faces_from_facets(fs):
    result={0}
    for f in fs:
        g=f
        while g:result.add(g);g=(g-1)&f
    return result

n=12
F=[sum(1<<x for x in c) for c in combinations(range(n),4)]
T=[sum(1<<x for x in c) for c in combinations(range(n),3)]
E=[sum(1<<x for x in c) for c in combinations(range(n),2)]
f=[z3.Bool('f%d'%i) for i in range(len(F))];t={g:z3.Bool('t%d'%g) for g in T};e={g:z3.Bool('e%d'%g) for g in E}
s=z3.Solver();s.set(timeout=10000,random_seed=42)
for h,var in list(t.items())+list(e.items()):s.add(var==z3.Or([f[i] for i,g in enumerate(F) if g&h==h]))
for i,g in enumerate(F):
    vs=[v for v in range(n) if g>>v&1];boundary=[t[g^(1<<v)] for v in vs]
    s.add(z3.Or(f[i],z3.PbLe([(x,1) for x in boundary],2)))
    for a,b in combinations(range(4),2):s.add(z3.Or(f[i],z3.Not(boundary[a]),z3.Not(boundary[b]),e[(1<<vs[a])|(1<<vs[b])]))
for v in range(n):s.add(z3.Or([f[i] for i,g in enumerate(F) if g>>v&1]))
s.add(z3.Not(z3.And(f)))
# Can fix one present facet by symmetry.
s.add(f[0])
start=time.time();cuts=set();count=0
for it in range(50000):
    res=s.check()
    if res!=z3.sat:print('RESULT',res,'iteration',it,'reason',s.reason_unknown(),flush=True);break
    m=s.model();fs=tuple(g for i,g in enumerate(F) if z3.is_true(m[f[i]]));C=faces_from_facets(fs);newcuts=[]
    for tau in C:
        if tau.bit_count()>2:continue
        L={g^tau for g in C if g&tau==tau}
        for i in range(3-tau.bit_count()):
            support=nonzero_homology_cochain(L,i)
            if support is None:continue
            possible=[]
            for j,g in enumerate(F):
                if g&tau!=tau:continue
                h=g^tau;vv=[v for v in range(n) if h>>v&1]
                if any(sum(1 for a in support if a&sub==a)%2 for sub in [sum(1<<v for v in cc) for cc in combinations(vv,i+2)]):possible.append(j)
            cut=tuple(possible)
            assert cut and not any(F[j] in fs for j in cut)
            if cut not in cuts:cuts.add(cut);newcuts.append(cut)
    if not newcuts:
        count+=1;print('CM CANDIDATE',it,len(fs),'facets',fs,flush=True)
        Path('workspace/a4_terminal_CM_%d.json'%count).write_text(json.dumps(fs))
        yes=kd(fs,2);print('shellable?',yes,flush=True)
        if yes:print('FOUND TRUE OBSTRUCTION',flush=True);break
        s.add(z3.Or([z3.Not(x) if F[j] in fs else x for j,x in enumerate(f)]))
    else:
        for cut in newcuts:s.add(z3.Or([f[j] for j in cut]))
    if it%100==0:print('iteration',it,'cuts',len(cuts),'time',time.time()-start,flush=True)
    if time.time()-start>100:break
Path('workspace/agent4_terminal_CM_sat.py').write_text(Path(__file__).read_text())
print('DONE',it,'cuts',len(cuts),'CM candidates',count,'seconds',time.time()-start,flush=True)
