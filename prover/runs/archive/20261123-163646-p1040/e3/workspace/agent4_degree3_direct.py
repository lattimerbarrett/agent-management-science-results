import sys,itertools,time
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_tensor import *
N=4;n=3
# Interleaved generator convention used in derivations and seed certificate.
desc=[]
for i in range(1,n+1):
 for j in range(1,n+1):
  if i!=j:desc.append(('K',i,j))
 for j,k in itertools.combinations([j for j in range(1,n+1) if j!=i],2):desc.append(('M',i,j,k))
gens={}
for q,d in enumerate(desc,1):
 typ,i,*js=d
 for sign in [1,-1]:
  im=[(k,) for k in range(1,n+1)]
  if typ=='K':
   j=js[0];im[i-1]=(sign*j,i,-sign*j)
  else:
   j,k=js;w=commutator_word((j,),(k,))
   if sign<0:w=inverse_word(w)
   im[i-1]=w+(i,)
  gens[sign*q]=tuple(add(magnus(w,N),{():1},-1) for w in im)
words=[w for d in range(1,N+1) for w in itertools.product(range(1,n+1),repeat=d)]
operators={}
for q,im in gens.items():
 op={():{():1}}
 for w in words:op[w]=mul(op[w[:-1]],im[w[-1]-1],N)
 operators[q]=op

def apply(q,p):
 out={}
 for w,c in p.items():out=add(out,operators[q][w],c)
 return out

def W(t):
 out=(t[0]+1,)
 for q in t[1:]:out=commutator_word(out,(q+1,))
 return out
terms=[((0,5,2),3),((0,2,5),-1),((0,1,1),-4),((1,2,3),-2)]
word=()
for t,a in terms:
 w=W(t)
 if a<0:w=inverse_word(w)
 word+=w*abs(a)
images=[{(i,):1} for i in range(1,n+1)]
for q in reversed(word):images=[apply(q,p) for p in images]
assert images==[{(i,):1} for i in range(1,n+1)]
print('Actual seed word length',len(word),'fixes all3 Magnus variables EXACTLY through degree',N)
