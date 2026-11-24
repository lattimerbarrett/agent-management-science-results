import sys,itertools,time,json,pathlib
import z3
from sage.all import Matrix,GF,VectorSpace,vector

def cm_cuts(n,F,p=2):
 V=set(range(n));cuts=[]
 # all links needing lower cohomology
 for tau in [()]+list(itertools.combinations(range(n),1))+list(itertools.combinations(range(n),2)):
  st=set(tau);L=[tuple(sorted(set(f)-st)) for f in F if st<=set(f)]
  if not L:continue
  E=sorted(V-st);dim=3-len(tau)
  face={j:sorted({s for f in L for s in itertools.combinations(f,j+1)}) for j in range(dim+1)}
  K=GF(p)
  for j in range(dim):
   fs=face[j];idx={f:i for i,f in enumerate(fs)};hs=face[j+1]
   rows=[]
   for h in hs:
    row=[0]*len(fs)
    for i in range(len(h)):row[idx[h[:i]+h[i+1:]]]=(-1)**i
    rows.append(row)
   A=Matrix(K,rows,ncols=len(fs));Z=A.right_kernel()
   W=VectorSpace(K,len(fs))
   if j==0:
    B=W.subspace([W([1]*len(fs))]);boundary=Matrix(K,[[1]*len(fs)])
   else:
    prev=face[j-1];ii={f:i for i,f in enumerate(prev)}
    rows=[]
    for f in fs:
     row=[0]*len(prev)
     for i in range(len(f)):row[ii[f[:i]+f[i+1:]]]=(-1)**i
     rows.append(row)
    cob=Matrix(K,rows,ncols=len(prev));B=cob.column_space();boundary=cob.transpose()
   for z in Z.basis():
    if z in B:continue
    B=B+W.subspace([z]);cut=[]
    for h in itertools.combinations(E,j+2):
     val=sum(((-1)**i)*z[idx[h[:i]+h[i+1:]]] for i in range(len(h)) if h[:i]+h[i+1:] in idx)
     if val:cut.append(tuple(sorted(st|set(h))))
    assert cut
    cycles=[c for c in boundary.right_kernel().basis() if c.dot_product(z)]
    assert cycles
    cycle=min(cycles,key=lambda c:sum(bool(x) for x in c))
    guard=[tuple(sorted(st|set(f))) for f,x in zip(fs,cycle) if x and len(st|set(f))>=3]
    cuts.append((cut,guard))
 return cuts

def search(n,seconds=30,maxmodels=100):
 V=range(n);tet=list(itertools.combinations(V,4));tri=list(itertools.combinations(V,3));ed=list(itertools.combinations(V,2))
 T={f:z3.Bool('t_'+str(f)) for f in tet};Q={f:z3.Bool('q_'+str(f)) for f in tri};s=z3.Solver();s.set(timeout=seconds*1000)
 for f in tet:
  qs=[Q[q] for q in itertools.combinations(f,3)]
  s.add(T[f]==z3.And(qs),z3.Implies(z3.Not(T[f]),z3.PbLe([(x,1) for x in qs],2)))
 for q in tri:s.add(z3.Implies(Q[q],z3.Or([T[f] for f in tet if set(q)<=set(f)])))
 for e in ed:s.add(z3.Or([T[f] for f in tet if set(e)<=set(f)]))
 s.add(T[0,1,2,3],z3.Not(T[0,1,2,4]))
 s.add(z3.PbGe([(x,1) for x in Q.values()],(n-2)**2))
 s.add(z3.Sum([z3.If(t,1,0) for t in T.values()])-z3.Sum([z3.If(q,1,0) for q in Q.values()])+len(ed)-n+1>=0)
 vars={**T,**Q};print('built',n,flush=True)
 for mnum in range(maxmodels):
  t=time.time();r=s.check();print(n,mnum,r,round(time.time()-t,3),flush=True)
  if r!=z3.sat:return
  m=s.model();F=[f for f in tet if z3.is_true(m[T[f]])]
  cuts=cm_cuts(n,F,2)
  if not cuts:cuts=cm_cuts(n,F,3)
  print('facets',len(F),'cuts',len(cuts),flush=True)
  if not cuts:
   out='workspace/agent2_CMtrap_'+str(n)+'.json';json.dump(F,open(out,'w'));print('CM TRAP SAVED',out,flush=True);return out
  for cut,guard in cuts:s.add(z3.Or([vars[f] for f in cut]+[z3.Not(vars[f]) for f in guard]))

if __name__=='__main__':
 pathlib.Path('workspace/agent2_CMtrap_cegar.py').write_text(pathlib.Path(__file__).read_text())
 for n in [8,9,10,11,12]:
  if search(n):break
