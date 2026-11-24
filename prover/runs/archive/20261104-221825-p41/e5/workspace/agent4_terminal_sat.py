from itertools import combinations
from pathlib import Path
import z3,random,time,sys,json
Path('workspace/agent4_terminal_sat.py').write_text(Path(__file__).read_text())
sys.path.insert(0,'workspace')
from exact_decomp_a4 import *
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
n=9
tri=list(combinations(range(n),3)); tet=list(combinations(range(n),4)); edges=list(combinations(range(n),2))
ti={t:i for i,t in enumerate(tri)};ei={e:i for i,e in enumerate(combinations(range(1,n),2))};q=len(ei)
vectors=[sum(1<<ei[E] for E in combinations(T,2) if 0 not in E) for T in tri]
t=[z3.Bool('t%d'%i) for i in range(len(tri))]; f=[z3.Bool('f%d'%i) for i in range(len(tet))]
s=z3.Solver();s.set(random_seed=41)
for i,F in enumerate(tet):
    boundary=[t[ti[T]] for T in combinations(F,3)]
    s.add(f[i]==z3.And(boundary))
    s.add(z3.Or(f[i],z3.PbLe([(x,1) for x in boundary],2)))
for j,T in enumerate(tri):s.add(t[j]==z3.Or([f[i] for i,F in enumerate(tet) if set(T)<=set(F)]))
for E in edges:s.add(z3.Or([f[i] for i,F in enumerate(tet) if set(E)<=set(F)]))
s.add(z3.Not(z3.And(f)))
s.set(timeout=10000)
start=time.time();cuts=set();stats={}
for it in range(20000):
    res=s.check()
    if res!=z3.sat:print('RESULT',res,'after',it,'reason',s.reason_unknown(),flush=True);break
    m=s.model(); mask=[z3.is_true(m[x]) for x in f]; ts=[i for i,x in enumerate(t) if z3.is_true(m[x])]
    ns=nullspace([vectors[j] for j in ts],q);h1=len(ns)
    stats[h1]=stats.get(h1,0)+1
    if not ns:
        fs=frozenset(frozenset(F) for F,x in zip(tet,mask) if x)
        print('H1ZERO',it,len(fs),list(map(sorted,fs)),flush=True)
        Path('workspace/a4_terminal_h1zero.json').write_text(json.dumps(list(map(sorted,fs))))
        print('shellable?',shellable(fs),flush=True)
        s.add(z3.Or([x!=v for x,v in zip(f,mask)]))
    else:
        for bits in range(1,1<<h1):
            u=0
            for j,v in enumerate(ns):
                if bits>>j&1:u^=v
            if u in cuts:continue
            cuts.add(u)
            s.add(z3.Or([t[j] for j,v in enumerate(vectors) if (v&u).bit_count()%2]))
    if it%100==0:print('iteration',it,'cuts',len(cuts),'h1',h1,'time',time.time()-start,flush=True)
    if time.time()-start>100:break
print('stats',stats,'cuts',len(cuts),'seconds',time.time()-start,flush=True)
