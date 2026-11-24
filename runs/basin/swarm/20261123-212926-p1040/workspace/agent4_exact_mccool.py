import sys,time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,'workspace')
from agent3_derivations import bracket
# Arithmetic via very large modulus isn't exact; use copied sparse tensor maps with no modulus.
def add(a,b,s):
 a=a.copy()
 for k,v in b.items():
  z=a.get(k,0)+s*v
  if z:a[k]=z
  elif k in a:del a[k]
 return a
def app(a,w):
 o={}
 for pos,x in enumerate(w):
  for (i,v),t in a.items():
   if i==x:
    k=w[:pos]+v+w[pos+1:];o[k]=o.get(k,0)+t
 return {k:v for k,v in o.items() if v}
def br(a,b):
 o={}
 for (i,w),v in b.items():
  for t,z in app(a,w).items():o[(i,t)]=o.get((i,t),0)+v*z
 for (i,w),v in a.items():
  for t,z in app(b,w).items():o[(i,t)]=o.get((i,t),0)-v*z
 return {k:v for k,v in o.items() if v}
def basis(vecs):
 piv={}
 for a in vecs:
  while a:
   k=min(a)
   if k in piv:a=add(a,piv[k],-a[k])
   else:
    c=a[k];piv[k]={t:Fraction(v,c) for t,v in a.items()};break
 return list(piv.values())
if __name__=='__main__':
 gs=[{(i,(j,i)):1,(i,(i,j)):-1} for i in range(3) for j in range(3) if i!=j]
 bs=gs;out=[6]
 for d in range(2,8):
  t=time.time();bs=basis(br(a,b) for a in gs for b in bs);out.append(len(bs));print(d,len(bs),time.time()-t,flush=True)
 Path('workspace/agent4_exact_mccool_output.txt').write_text(repr(out))
