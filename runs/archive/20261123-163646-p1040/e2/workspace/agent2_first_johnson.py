import sys
sys.path.insert(0,'workspace')
from agent2_freewords import mag, inv
from agent2_derivations import add,scale

def product(a,b,M):
 out={}
 for u,c in a.items():
  for v,d in b.items():
   if len(u)+len(v)<=M:out[u+v]=out.get(u+v,0)+c*d
 return {w:c for w,c in out.items() if c}
def expand(w,M):
 out={():1}
 for x in w:
  i=abs(x)-1
  f={():1,(i,):1} if x>0 else {(i,)*k:(-1)**k for k in range(M+1)}
  out=product(out,f,M)
 return out
for n in range(2,9):
 G=mag(n)
 images=[]
 for (i,j,k),phi,phiinv in G:
  for l in range(n):
   delta=phi[l]+(-(l+1),)
   v=expand(delta,2);v.pop((),None)
   expected={(j,k):1,(k,j):-1} if l==i else {}
   assert v==expected,((i,j,k),l,v,expected)
  images.append((i,j,k))
 assert len(images)==n*n*(n-1)//2 and len(set(images))==len(images)
 print('n=',n,'Magnus first Johnson basis verified:',len(images))
