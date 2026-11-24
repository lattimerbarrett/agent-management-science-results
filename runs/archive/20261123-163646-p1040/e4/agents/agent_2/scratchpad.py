import itertools, pickle, time, os

def red(w):
 s=[]
 for x in w:
  if s and s[-1]==-x:s.pop()
  else:s.append(x)
 return tuple(s)
def inv(w):return tuple(-x for x in w[::-1])
def mul(*ws):return red(sum((tuple(w) for w in ws),()))
def substitute(w,A):return mul(*(A[x-1] if x>0 else inv(A[-x-1]) for x in w))
def comp(A,B):return tuple(substitute(w,A) for w in B)
I=((1,),(2,),(3,))
gens=[]; names=[]
for i in range(3):
 for j in range(3):
  if i==j:continue
  A=list(I); A[i]=(j+1,i+1,-j-1);gens.append(tuple(A));names.append(('C',i,j))
for i in range(3):
 j,k=[j for j in range(3) if j!=i]
 A=list(I);A[i]=mul((j+1,k+1,-j-1,-k-1),I[i]);gens.append(tuple(A));names.append(('T',i,j,k))
# Inverses by changing conjugator / commutator to inverse.
for data in names:
 A=list(I)
 if data[0]=='C':
  _,i,j=data;A[i]=(-j-1,i+1,j+1)
 else:
  _,i,j,k=data;A[i]=mul((k+1,j+1,-k-1,-j-1),I[i])
 gens.append(tuple(A))
assert all(comp(gens[i],gens[i+9])==I for i in range(9))
letters=list(range(1,10))+list(range(-1,-10,-1))
G={x:gens[x-1 if x>0 else 8-x] for x in letters}
seen={I:()}; level=[(I,())]; rel=[]
for d in range(1,5):
 nxt=[]
 for A,w in level:
  for x in letters:
   if w and w[-1]==-x:continue
   v=w+(x,);B=comp(A,G[x])
   if B in seen:
    r=mul(v,inv(seen[B]))
    if r:rel.append(r)
   else:seen[B]=v;nxt.append((B,v))
 level=nxt
 print('length',d,'states',len(seen),'relations',len(rel),flush=True)
J=[]
for j in range(3):
 J.append(tuple(k+1 for k,data in enumerate(names) if data[0]=='C' and data[2]==j))
for gi,g in enumerate(gens[:9]):
 for j in range(3):
  rhs=mul(*(J[x-1] if x>0 else inv(J[-x-1]) for x in g[j]))
  rel.append(mul((gi+1,),J[j],(-gi-1,),inv(rhs)))
os.makedirs('workspace',exist_ok=True)
pickle.dump((names,rel),open('workspace/agent2_shortrels.pkl','wb'))
print('relation lengths', {d:sum(len(r)==d for r in rel) for d in range(1,7)})
Ts=[(((2,),(1,),(3,)),((2,),(1,),(3,))),(((2,),(3,),(1,)),((3,),(1,),(2,))),(((-1,),(2,),(3,)),((-1,),(2,),(3,))),(((1,2),(2,),(3,)),((1,-2),(2,),(3,)))]
Maps=[]
for t,ti in Ts:
 ims=[]
 for g in gens[:9]:
  a=comp(comp(t,g),ti)
  w=seen.get(a)
  if w is None:
   for b,v in seen.items():
    aa=comp(a,b)
    if aa in seen:
     w=mul(seen[aa],inv(v));break
  ims.append(w)
 print('Nielsen images',ims,flush=True)
 Maps.append(ims)
import numpy as np
p=1000003
basis={}
def addrow(v):
 v=v.copy()%p
 for j,b in sorted(basis.items()):
  if v[j]:v=(v-int(v[j])*b)%p
 nz=np.flatnonzero(v)
 if not len(nz):return False
 j=int(nz[0]);v=v*pow(int(v[j]),-1,p)%p;basis[j]=v;return True

def magnus(w):
 out={():1}
 for x in w:
  i=abs(x)-1
  terms={():1,(i,):1} if x>0 else {tuple([i]*k):(-1)**k for k in range(4)}
  nxt={}
  for a,c in out.items():
   for b,d in terms.items():
    if len(a+b)<=3:nxt[a+b]=nxt.get(a+b,0)+c*d
  out={a:c for a,c in nxt.items() if c}
 assert not any(len(a)==1 for a in out)
 return out
M=[magnus(r) for r in rel]
# append [X_i, rel_degree2]
for m in M:
 for i in range(9):
  v=np.zeros(810,dtype=np.int64)
  for w,c in m.items():
   if len(w)==2:
    a,b=w;v[81+i*81+a*9+b]+=c;v[81+a*81+b*9+i]-=c
  addrow(v)
print('bracket ideal rank',len(basis),flush=True)
def vec(m):
 v=np.zeros(810,dtype=np.int64)
 for w,c in m.items():
  if len(w)==2:v[w[0]*9+w[1]]=c
  elif len(w)==3:v[81+w[0]*81+w[1]*9+w[2]]=c
 return v
queue=[]
for r,m in zip(rel,M):
 if addrow(vec(m)):queue.append(r)
print('seed rels',len(queue),flush=True)
qi=0
while qi<len(queue):
 r=queue[qi];qi+=1
 for mp in Maps[:3]:
  s=mul(*(mp[x-1] if x>0 else inv(mp[-x-1]) for x in r))
  if addrow(vec(magnus(s))):queue.append(s)
print('signed perm closure',len(basis),'accepted rels',len(queue),flush=True)
r2=sum(j<81 for j in basis)
print('total rank',len(basis),'quadratic rank',r2,'central rank',len(basis)-r2,'gr3 upper bound',240-(len(basis)-r2),flush=True)
