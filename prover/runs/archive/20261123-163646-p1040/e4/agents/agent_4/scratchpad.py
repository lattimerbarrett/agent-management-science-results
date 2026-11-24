import pickle
from collections import defaultdict
from sympy import Matrix

def red(w):
 s=[]
 for a in w:
  if s and s[-1]==-a:s.pop()
  else:s.append(a)
 return tuple(s)
def inv(w):return tuple(-a for a in w[::-1])
def subst(w,images):
 return red(tuple(b for a in w for b in (images[a-1] if a>0 else inv(images[-a-1]))))
def comp(A,B):return tuple(subst(w,A) for w in B)
def auto_for(g,sign=1):
 A=[(1,),(2,),(3,)];typ,i,*jk=g
 if typ=='C':
  j=jk[0];A[i]=red((sign*(j+1),i+1,-sign*(j+1)))
 else:
  j,k=jk;v=(j+1,k+1,-j-1,-k-1);A[i]=red((v if sign==1 else inv(v))+(i+1,))
 return tuple(A)
G=[('C',i,j) for i in range(3) for j in range(3) if i!=j]+[('T',i,*[j for j in range(3) if j!=i]) for i in range(3)]
autos={s*(i+1):auto_for(g,s) for i,g in enumerate(G) for s in [1,-1]}
I={j:tuple(i+1 for i,g in enumerate(G) if g[0]=='C' and g[2]==j) for j in range(3)}
rels=[]
for a,g in enumerate(G,1):
 phi=autos[a]
 for j in range(3):
  rhs=subst(phi[j],tuple(I[k] for k in range(3)))
  rel=red((a,)+I[j]+(-a,)+inv(rhs))
  A=((1,),(2,),(3,))
  for b in rel:A=comp(A,autos[b])
  assert A==((1,),(2,),(3,)),(g,j,rel,A)
  if rel:rels.append(rel)
print('verified equivariance relations:',len(rels),'max length',max(map(len,rels)))
pickle.dump((G,rels),open('workspace/agent4_inner_relators.pkl','wb'))
open('workspace/agent4_inner_relators.py','w').write(open(__file__).read())
print(G);print(rels)
