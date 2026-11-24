import itertools,z3

def getpatterns(L):
 sets=set(itertools.combinations(range(L),2))
 for i in range(L):
  for j in range(i+1,L):
   s=tuple(sorted({(i-1)%L,i,(j-1)%L,j}))
   if len(s)==4:sets.add(s)
 sets.add(())
 out=[]
 for de in sets:
  de=set(de)
  for first in [0,1]:
   cs=[first]
   for i in range(L-1):cs.append(cs[-1] if i in de else 1-cs[-1])
   if (cs[-1]==cs[0])!=((L-1) in de):continue
   A={i for i in range(L) if cs[i]};ae=[i for i in de if cs[i]];be=[i for i in de if not cs[i]]
   out.append((A,ae,be))
 return out

def ispath2(es,L):return len(es)<2 or len(es)==2 and ((es[0]-es[1])%L in [1,L-1])
for L in range(10,61,2):
 xs=[z3.Bool('x'+str(i)) for i in range(L)];s=z3.Solver();s.set(timeout=15000)
 s.add(z3.PbEq([(xs[i],1) for i in range(0,L,2)],3),z3.PbEq([(xs[i],1) for i in range(1,L,2)],3))
 matching=[];tri=[]
 pats=getpatterns(L)
 for A,ae,be in pats:
  asum=z3.Sum([z3.If(xs[i],1,0) for i in A])
  if len(ae)==2 and not be and not ispath2(ae,L):matching.append(z3.And([z3.Not(xs[i]) for i in range(L) if i not in A]))
  if len(ae)==1 and len(be)==1:
   i=ae[0];tri.append(z3.And(xs[i],xs[(i+1)%L],asum==2))
  if not ispath2(be,L):continue
  if not ae:s.add(asum>=3)
  elif len(ae)==1:
   i=ae[0];s.add(asum!=0,z3.Not(z3.And(asum==1,z3.Or(xs[i],xs[(i+1)%L]))))
  elif len(ae)==2 and ispath2(ae,L):s.add(asum!=0)
 s.add(z3.Or(matching),z3.Or(tri))
 ans=s.check();print('L',L,'answer',ans,flush=True)
 if ans==z3.sat:
  mo=s.model();N=[i for i,x in enumerate(xs) if z3.is_true(mo[x])];print('FOUND Nv',N,flush=True);break
