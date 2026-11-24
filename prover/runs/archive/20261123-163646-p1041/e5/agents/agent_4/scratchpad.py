import numpy as np,itertools,json
def parts(total,k,lo=1):
 if k==1:
  if total>=lo:yield (total,)
 else:
  for i in range(lo,total//k+1):
   for r in parts(total-i,k-1,i):yield (i,)+r
for ns in sorted(parts(14,6),key=lambda ns:sum(n*n for n in ns)):
 deg=[sum(ns[i] for i in range(6) if t>>i&1) for t in range(64)]
 allowed=[t for t in range(64) if deg[t]<=7]
 pairs=[(t,t^63) for t in range(64) if deg[t]==7 and t<(t^63)]
 if not pairs:continue
 mb={mo:sum(1<<t for t in range(64) if t&mo==mo) for mo in allowed}
 code=[];descr=[]
 for aa,bb in pairs:
  rest=[t for t in allowed if t not in (aa,bb)]
  for adds in itertools.chain.from_iterable(itertools.combinations(rest,k) for k in range(6)):
   ts=(aa,bb)+adds;v=0
   for mo in ts:v^=mb[mo]
   code.append(v);descr.append(ts)
 code=np.array(code,dtype=np.uint64)
 indices=[((code>>np.uint64(8*j))&255).astype(np.uint8) for j in range(8)]
 ws=list(itertools.product(*(range(1,1<<n,2) for n in ns)))
 for w in ws:
  counts=[int(np.prod([w[i] if t>>i&1 else (1<<ns[i])-w[i] for i in range(6)])) for t in range(64)]
  result=np.zeros(len(code),dtype=np.int32)
  for j in range(8):
   tab=np.array([sum(counts[8*j+i] for i in range(8) if z>>i&1) for z in range(256)],dtype=np.int32)
   result+=tab[indices[j]]
  found=np.flatnonzero(result==310)
  if len(found):
   qi=int(found[0]);print('FOUND310GROUP6',ns,w,descr[qi],flush=True);raise SystemExit
 print('donegroup6',ns,len(code),flush=True)
print('nogroup6sparse');raise SystemExit
for ns in parts(14,5):
 deg=[sum(ns[i] for i in range(5) if t>>i&1) for t in range(32)]
 allowed=[t for t in range(32) if deg[t]<=7]
 pairs=[(t,t^31) for t in range(32) if deg[t]==7 and t<(t^31)]
 if not pairs:continue
 print(ns,len(allowed),len(pairs))
 # Exhaust all outer weighted-degree-seven polynomials via uint32 truth tables.
 base=[]
 for mo in allowed:
  base.append(sum((1<<t) for t in range(32) if t&mo==mo))
 code=np.zeros(1<<len(base),dtype=np.uint32)
 for i,v in enumerate(base): code[1<<i:1<<(i+1)]=code[:1<<i]^v
 indices=[((code>>np.uint32(8*j))&255).astype(np.uint8) for j in range(4)]
 ws=list(itertools.product(*(range(1,1<<n,2) for n in ns)))
 for w in ws:
  counts=[int(np.prod([w[i] if t>>i&1 else (1<<ns[i])-w[i] for i in range(5)])) for t in range(32)]
  result=np.zeros(len(code),dtype=np.int32)
  for j in range(4):
   tab=np.array([sum(counts[8*j+i] for i in range(8) if z>>i&1) for z in range(256)],dtype=np.int32)
   result+=tab[indices[j]]
  found=np.flatnonzero(result==310)
  if len(found):
   qi=int(found[0]);print('FOUND310FULLGROUP5',ns,w,[allowed[i] for i in range(len(allowed)) if qi>>i&1],flush=True);raise SystemExit
 print('full done',ns,flush=True)
 continue
 pols=[]; descriptions=[]
 for aa,bb in pairs:
  rest=[t for t in allowed if t not in (aa,bb)]
  for adds in itertools.chain.from_iterable(itertools.combinations(rest,k) for k in range(5)):
   ts=(aa,bb)+adds
   pols.append([sum(t&mo==mo for mo in ts)%2 for t in range(32)])
   descriptions.append(ts)
 truth=np.array(pols,dtype=np.int64)
 ws=list(itertools.product(*(range(1,1<<n,2) for n in ns)))
 counts=np.array([[np.prod([w[i] if t>>i&1 else (1<<ns[i])-w[i] for i in range(5)]) for t in range(32)] for w in ws],dtype=np.int64)
 weights=truth@counts.T
 found=np.argwhere(weights==310)
 if len(found):
  qi,wi=map(int,found[0]);print('FOUND310GROUP5',ns,ws[wi],descriptions[qi],flush=True);raise SystemExit
print('nogroup5fourterms')
raise SystemExit
for a in range(1,7):
 for b in range(a,7):
  ns=(a,7-a,b,7-b)
  mons=[0]+[1<<i for i in range(4)]+[(1<<i)|(1<<j) for i in range(4) for j in range(i+1,4) if ns[i]+ns[j]<=7]
  masks=np.array([[int(t&mo==mo) for t in range(16)] for mo in mons],dtype=np.int64)
  co=np.array([[z>>i&1 for i in range(len(mons))] for z in range(1<<len(mons))],dtype=np.int64)
  truth=co@masks%2
  ws=list(itertools.product(*(range(1,1<<n,2) for n in ns)))
  counts=np.array([[np.prod([w[i] if t>>i&1 else (1<<ns[i])-w[i] for i in range(4)]) for t in range(16)] for w in ws],dtype=np.int64)
  weights=truth@counts.T
  found=np.argwhere(weights==310)
  if len(found):
   qi,wi=map(int,found[0]); print('FOUND310groups',ns,ws[wi],[mons[i] for i in range(len(mons)) if qi>>i&1],flush=True)
   raise SystemExit
print('no4group construction',flush=True)
raise SystemExit
import z3,time
P4=[(a,b) for a in range(1,16) for b in range(1,16)]
ch4=[(a,b) for a in range(1,16) for b in range(1,16) if a.bit_count()+b.bit_count()<=4]
zs=[z3.Bool('p%d'%i) for i in range(225)]
sol=z3.Solver(); sol.set(timeout=240000)
for a,b in ch4:
 sel=[zs[i] for i,(x,y) in enumerate(P4) if x&a==a and y&b==b]
 sol.add(z3.Not(__import__('functools').reduce(z3.Xor,sel)))
sol.add(z3.PbEq([(v,1) for v in zs],14))
print('Z3 result',sol.check(),flush=True)
if sol.check()==z3.sat:
 model=sol.model();found=[P4[i] for i,z in enumerate(zs) if z3.is_true(model.eval(z))]
 print('FOUND14',found,flush=True)
 open('workspace/agent4_14points.json','w').write(__import__('json').dumps(found))
import itertools
from sage.all import Matrix,GF
P=[(a,b) for a in range(1,8) for b in range(1,8)]
checks=[(a,b) for a in range(1,8) for b in range(1,8) if a.bit_count()+b.bit_count()<=4]
M=Matrix(GF(2),[[int((x&a)==a and (y&b)==b) for x,y in P] for a,b in checks])
ker=M.right_kernel().basis(); print('kernel dim',len(ker))
for mask in range(1,1<<len(ker)):
 v=sum((ker[i] for i in range(len(ker)) if mask>>i&1),ker[0]*0)
 if sum(map(int,v))==14:
  print('FOUND14', [P[i] for i in range(49) if v[i]])
  break
import json
D=json.load(open('workspace/agent3_low_witnesses.json'))
from itertools import product
flats=D['308']
def pts(basis,shift):
 p=[shift]
 for b in basis:p += [x^b for x in p]
 return p
S=set()
for basis,shift in flats:S.symmetric_difference_update(pts(basis,shift))
for fi,(basis,shift) in enumerate(flats):
 p=pts(basis,shift)
 for normal in range(1,128):
  for rhs in (0,1):
   F=[p[x] for x in range(128) if (x&normal).bit_count()%2==rhs]
   if sum(x in S for x in F)==63:
    print('FOUND310',fi,normal,rhs,F)
print('near-flat search complete')
import runpy
runpy.run_path('workspace/agent2_central_certificate.py',run_name='__main__')
runpy.run_path('workspace/agent4_autocorrelation.py',run_name='__main__')
from itertools import product
D={}
for t in range(8):
 for a,b,c in product(range(t,8),repeat=3):
  hmax=min(7-a-b+t,7-a-c+t,7-b-c+t)
  hmin=max(0,7-a-b-c+t)
  if hmax<hmin:continue
  w=384-2*((1<<a)+(1<<b)+(1<<c))+4*(1<<t)
  if 0<w<336 and w%4==2:
   D.setdefault(w,[]).append((a,b,c,t,hmin,hmax))
print(D)
import random
for m,r in [(5,3),(7,4),(9,5)]:
 ds=[]
 for trial in range(20):
  mons=[mask for mask in range(1<<m) if mask.bit_count()<=r and random.getrandbits(1)]
  f=[sum((x&z)==z for z in mons)%2 for x in range(1<<m)]
  q=[sum(f[x]*f[x^v] for x in range(1<<m))//2%2 for v in range(1<<m)]
  for i in range(m):
   for v in range(1<<m):
    if v>>i&1:q[v]^=q[v^(1<<i)]
  ds.append(max([v.bit_count() for v in range(1<<m) if q[v]] or [-1]))
 print(m,r,ds)

# Save reusable exact autocorrelation-ANF checker.
from pathlib import Path
Path('workspace/agent4_autocorrelation.py').write_text('''"""Exact check of the autocorrelation degree lemma on supplied ANF masks."""
from itertools import combinations

def autocorrelation_check(m, masks):
    masks=tuple(masks)
    assert len(set(masks))==len(masks)
    r=max((a.bit_count() for a in masks),default=0)
    assert r<=m-2
    f=[sum((x&a)==a for a in masks)%2 for x in range(1<<m)]
    aa=[sum(f[x]*f[x^v] for x in range(1<<m)) for v in range(1<<m)]
    assert all(a%2==0 for a in aa)
    q=[(a//2)%2 for a in aa]
    predicted=[]
    full=(1<<m)-1
    for v in range(1<<m):
        z=0
        for a,b in combinations(masks,2):
            # Correlation has odd size precisely when the union covers all
            # variables and v vanishes on the intersection.
            if a|b==full and v&(a&b)==0: z^=1
        predicted.append(z)
    assert q==predicted
    anf=q[:]
    for i in range(m):
        for v in range(1<<m):
            if v>>i&1: anf[v]^=anf[v^(1<<i)]
    assert all(not z or v.bit_count()<=2*r-m for v,z in enumerate(anf))
    return aa,anf

if __name__=='__main__':
    import random
    rng=random.Random(20260714)
    for m,r in [(4,2),(5,3),(6,3),(7,4)]:
        candidates=[a for a in range(1<<m) if a.bit_count()<=r]
        for j in range(20):
            masks=[a for a in candidates if rng.randrange(2)]
            autocorrelation_check(m,masks)
    print('80 exact autocorrelation identity and degree checks passed')
''')
