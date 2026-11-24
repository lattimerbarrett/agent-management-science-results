from collections import defaultdict
from pathlib import Path

def red(w):
 a=[]
 for x in w:
  if a and a[-1]==-x:a.pop()
  else:a.append(x)
 return tuple(a)
def inv(w):return tuple(-x for x in w[::-1])
def comm(a,b):return red(a+b+inv(a)+inv(b))
def add(a,b,s=1):
 c=defaultdict(int,a)
 for w,v in b.items():c[w]+=s*v
 return {w:v for w,v in c.items() if v}
def mul(a,b,d=4):
 c=defaultdict(int)
 for u,v in a.items():
  for w,z in b.items():
   if len(u+w)<=d:c[u+w]+=v*z
 return {w:v for w,v in c.items() if v}
def mag(w):
 a={():1}
 for x in w:
  f={():1,(abs(x),):1} if x>0 else {tuple([abs(x)]*k):(-1)**k for k in range(5)}
  a=mul(a,f)
 return a
names=[('K',1,2),('K',1,3),('M',1,2,3),('K',2,1),('K',2,3),('M',2,1,3),('K',3,1),('K',3,2),('M',3,1,2)]
def maps(g,sgn):
 ty,i,*jk=names[g]; out=[{(k,):1} for k in (1,2,3)]
 if ty=='K':
  j=jk[0];w=(sgn*j,i,-sgn*j)
 else:
  j,k=jk;h=(j,k,-j,-k);w=(h if sgn>0 else inv(h))+(i,)
 out[i-1]=add(mag(w),{():1},-1)
 return out
G={s*(i+1):maps(i,s) for i in range(9) for s in (-1,1)}
def subst(p,im):
 out={}
 for w,c in p.items():
  a={():c}
  for k in w:a=mul(a,im[k-1])
  out=add(out,a)
 return out

def W(i,j,k):return comm(comm((i+1,),(j+1,)),(k+1,))
terms=[((0,5,2),3),((0,2,5),-1),((0,1,1),-4),((1,2,3),-2)]
w=()
for inds,c in terms:
 t=W(*inds);t=t if c>0 else inv(t);w=red(w+t*abs(c))
im=[{(i,):1} for i in (1,2,3)]
for a in w[::-1]:im=[subst(p,G[a]) for p in im]
print('wordlength',len(w),'fixedthrough4',im==[{(i,):1} for i in (1,2,3)])
assert im==[{(i,):1} for i in (1,2,3)]
