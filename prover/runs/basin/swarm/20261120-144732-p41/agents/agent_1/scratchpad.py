from itertools import combinations
import time,z3

def bits(x):
 while x:
  b=x&-x;yield b;x-=b

def subsets(x,r):return [sum(c) for c in combinations(list(bits(x)),r)]
def norm(fs):
 fs=set(fs)
 return tuple(sorted(f for f in fs if not any(f!=g and f&g==f for g in fs)))
def reduce_row(x,B):
 while x:
  p=x&-x
  if p not in B:break
  x^=B[p]
 return x

def obstruction(fs,j):
 J=sorted(set(a for f in fs for a in subsets(f,j+1)))
 P=sorted(set(a for f in fs for a in subsets(f,j)))
 Q=sorted(set(a for f in fs for a in subsets(f,j+2)))
 ix={a:i for i,a in enumerate(J)};ip={a:i for i,a in enumerate(P)}
 boundary=[sum(1<<ix[q^b] for b in bits(q)) for q in Q]
 B={}
 for r in boundary:
  r=reduce_row(r,B)
  if r:B[r&-r]=r
 K={};z=None
 for i,a in enumerate(J):
  r=sum(1<<ip[a^b] for b in bits(a));c=1<<i
  while r:
   p=r&-r
   if p not in K:break
   r^=K[p][0];c^=K[p][1]
  if r:K[r&-r]=(r,c)
  elif reduce_row(c,B):z=c;break
 if z is None:return None
 equations={}
 for r,rhs in [(b,0) for b in boundary]+[(z,1)]:
  while r:
   p=r&-r
   if p not in equations:break
   a,b=equations[p];r^=a;rhs^=b
  if not r:assert rhs==0
  else:equations[r&-r]=(r,rhs)
 w=0
 for p in sorted(equations,reverse=True):
  r,rhs=equations[p]
  if ((r&w).bit_count()&1)^rhs:w|=p
 assert (w&z).bit_count()%2==1
 assert all((w&b).bit_count()%2==0 for b in boundary)
 return [J[i] for i in range(len(J)) if z>>i&1],set(J[i] for i in range(len(J)) if w>>i&1)

def components(fs):
 V=set(b for f in fs for b in bits(f));out=[]
 while V:
  C={V.pop()};change=True
  while change:
   change=False
   for f in fs:
    vs=set(bits(f))
    if vs&C and not vs<=C:C|=vs;change=True
  V-=C;out.append(C)
 return out

n=9;V=(1<<n)-1;F=subsets(V,4);T=subsets(V,3);E=subsets(V,2)
y={f:z3.Bool('F'+str(f)) for f in F};t={a:z3.Bool('T'+str(a)) for a in T};ev={a:z3.Bool('E'+str(a)) for a in E}
s=z3.Solver();s.set(timeout=20000)
for a in T:s.add(t[a]==z3.Or([y[f] for f in F if f&a==a]))
for a in E:s.add(ev[a]==z3.Or([y[f] for f in F if f&a==a]))
for v in bits(V):s.add(z3.Or([y[f] for f in F if f&v]))
for f in F:
 block=[]
 for a in subsets(f,2):block.append(z3.And(ev[a],*[z3.Not(t[b]) for b in subsets(f,3) if b&a==a]))
 for v in bits(f):block.append(z3.And(*[z3.Not(t[b]) for b in subsets(f,3) if b&v]))
 s.add(z3.Implies(z3.Not(y[f]),z3.Or(block)))
s.add(y[F[0]],y[F[1]],z3.Or([z3.Not(y[f]) for f in F]))
S=lambda a:z3.Sum([z3.If(v,1,0) for v in a])
s.add(S(ev.values())-3*n+6>=0,S(t.values())-2*S(ev.values())+3*n-4>=0,S(y.values())-S(t.values())+S(ev.values())-n+1>=0)
for v in bits(V):
 tv=[t[a] for a in T if a&v];fv=[y[a] for a in F if a&v];ee=[ev[a] for a in E if a&v]
 s.add(S(ee)>=3,S(tv)-2*S(ee)+3>=0,S(fv)-S(tv)+S(ee)-1>=0)
for e in E:s.add(S([y[a] for a in F if a&e==e])-S([t[a] for a in T if a&e==e])+1>=0)

def facevar(a):
 r=a.bit_count()
 if r<=1:return z3.BoolVal(True)
 if r==2:return ev[a]
 if r==3:return t[a]
 if r==4:return y[a]
 raise ValueError(a)

def homology_cut(fs,j,tau):
 ob=obstruction(fs,j)
 if ob is None:return None
 cycle,w=ob
 clause=[z3.Not(facevar(tau|a)) for a in cycle]
 for a in subsets(V^tau,j+2):
  if sum((a^b) in w for b in bits(a))%2:clause.append(facevar(tau|a))
 return z3.Or(clause)

def connectivity_cut(fs,tau):
 cs=components(fs)
 if len(cs)<=1:return None
 A=cs[0];B=set().union(*cs[1:])
 clause=[z3.Not(facevar(tau|next(iter(A)))),z3.Not(facevar(tau|next(iter(B))))]
 AM=sum(A);allothers=(V^tau)^AM
 clause.extend(facevar(tau|a|b) for a in A for b in bits(allothers))
 return z3.Or(clause)

start=time.time();cuts=0;orders=False;types={}
for it in range(10000):
 status=s.check()
 if status!=z3.sat:
  print('status',status,'iterations',it,'cuts',cuts,'elapsed',time.time()-start,flush=True)
  if status==z3.unknown and time.time()-start<580:continue
  break
 model=s.model();fs=tuple(f for f in F if z3.is_true(model.eval(y[f])))
 new=[]
 c=connectivity_cut(fs,0)
 if c is not None:new.append(c)
 for j in (1,2):
  c=homology_cut(fs,j,0)
  if c is not None:
   new.append(c);types['global'+str(j)]=types.get('global'+str(j),0)+1
 for v in bits(V):
  L=norm(f^v for f in fs if f&v)
  c=connectivity_cut(L,v)
  if c is not None:new.append(c)
  c=homology_cut(L,1,v)
  if c is not None:
   new.append(c);types['vertex1']=types.get('vertex1',0)+1
 for e in E:
  L=norm(f^e for f in fs if f&e==e)
  c=connectivity_cut(L,e)
  if c is not None:
   new.append(c);types['edge0']=types.get('edge0',0)+1
 if new:
  s.add(new);cuts+=len(new)
 else:
  print('CM over F2 candidate:',it,len(fs),fs,flush=True)
  if orders:
   print('FOUND SHELLABLE TRAP',flush=True);break
  o={f:z3.Int('R'+str(f)) for f in F}
  for f in F:
   s.add(o[f]>=0,o[f]<len(F))
   if f==F[0]:s.add(o[f]==0)
   elif f==F[1]:s.add(o[f]==1)
   else:s.add(z3.Implies(y[f],o[f]>=2))
   neigh=[p for p in F if (p&f).bit_count()==3]
   if f!=F[0]:s.add(z3.Implies(y[f],z3.Or([z3.And(y[p],o[p]<o[f]) for p in neigh])))
   for g in F:
    if f==g or (f&g).bit_count()==3:continue
    h=f&g
    s.add(z3.Implies(z3.And(y[f],y[g],o[g]<=o[f]),z3.Or([z3.And(y[p],o[p]<o[f]) for p in neigh if p&h==h])))
  orders=True
 if it%50==0:print('progress',it,'cuts',cuts,'facets',len(fs),'elapsed',time.time()-start,flush=True)
 if time.time()-start>580:break
print('obstruction types',types)
