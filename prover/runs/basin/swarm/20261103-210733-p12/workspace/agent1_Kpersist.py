from functools import lru_cache
import pickle,time,os
KSTORE={};NSTORE={};CACHE_FILE=None;NEWMISS=0;LASTSAVE=time.time()
def save(path=None):
 global LASTSAVE
 path=path or CACHE_FILE
 if path:
  with open(path+'.tmp','wb') as f:pickle.dump((KSTORE,NSTORE),f,protocol=pickle.HIGHEST_PROTOCOL)
  os.replace(path+'.tmp',path);LASTSAVE=time.time()
def load(path):
 global KSTORE,NSTORE
 with open(path,'rb') as f:data=pickle.load(f)
 if isinstance(data,tuple):KSTORE.update(data[0]);NSTORE.update(data[1])
 elif isinstance(data,dict) and '_K' in data:KSTORE.update(data['_K']);NSTORE.update(data['node'])
 else:
  for (g,k,ds),v in data.items():
   aa=tuple(d-1 for d in ds if d>=2);low=[d for d in ds if d<2]
   if not low:KSTORE[g,k,aa]=v
   elif len(low)==1:NSTORE[g,k,aa,low[0]]=v
 print('loaded persistent states',len(KSTORE),len(NSTORE),flush=True)
def memo(which):
 def decorate(fn):
  def inner(*key):
   global NEWMISS
   store=KSTORE if which=='K' else NSTORE
   if key in store:return store[key]
   value=fn(*key);store[key]=value;NEWMISS+=1
   if NEWMISS%250000==0:
    print('newstates',NEWMISS,'K',len(KSTORE),'node',len(NSTORE),flush=True)
    if CACHE_FILE and time.time()-LASTSAVE>60:save()
   return value
  return lru_cache(maxsize=100000)(inner)
 return decorate

from collections import Counter
from itertools import product
from math import comb,factorial,prod
from agent1_hodge_mod import P,Q,b
from sympy import bernoulli
BERN={m:Q(bernoulli(m+1),m+1) for m in range(1,50,2)}
INV={k:pow(k,-1,P) for k in range(1,51)}
HALF=INV[2]
FACT=[factorial(i)%P for i in range(110)]
IFACT=[pow(x,-1,P) for x in FACT]
@lru_cache(None)
def top(g):return Q(abs(bernoulli(2*g)),2**(2*g-1)*factorial(2*g))
@lru_cache(None)
def odf(n):return prod(range(n,0,-2))%P
@lru_cache(maxsize=128)
def splits(a):
 cc=Counter(a);ks=tuple(cc);cs=tuple(cc.values());out=[]
 for vv in product(*(range(c+1) for c in cs)):
  aa=tuple(x for x,c in zip(ks,vv) for _ in range(c));bb=tuple(x for x,c,v in zip(ks,cs,vv) for _ in range(c-v))
  mult=prod(comb(c,v) for c,v in zip(cs,vv));out.append((aa,bb,mult,sum(aa)))
 return out

def K(g,k,a):
 if not 0<=k<g or sum(a)!=2*g-3-k:return 0
 return _K(g,k,tuple(sorted(a)))

@memo("node")
def node(g,k,a,r):
 n=len(a)
 if k==0:return b(g)*FACT[sum(a)+n+r]*prod(IFACT[x+1] for x in a)*IFACT[r]%P
 if r==0:
  out=0
  for x,c in Counter(a).items():
   aa=list(a);aa.remove(x)
   if x==1:out+=c*(2*g-3+n)*K(g,k,tuple(aa))
   else:aa.append(x-1);out+=c*K(g,k,tuple(aa))
  return out%P
 if r==1:return (2*g-2+n)*K(g,k,a)%P
 return K(g,k,a+(r-1,))

@memo("K")
def _K(g,k,a):
 n=len(a);A=sum(a)
 if k==0:return b(g)*FACT[A+n]*prod(IFACT[x+1] for x in a)%P
 if k==g-1:return top(g)*FACT[2*g-3+n]*pow(prod(odf(2*x+1) for x in a)%P,-1,P)%P
 out=0
 ct=Counter(a)
 for m in range(k if k%2 else k-1,0,-2):
  kk=k-m
  v=K(g,kk,a+(m,))
  for x,c in ct.items():
   aa=list(a);aa.remove(x);aa.append(x+m);v-=c*K(g,kk,tuple(aa))
  boundary=0
  for aa,bb,mult,Aa in splits(a):
   Ab=A-Aa
   glo=max(1,(Aa+3)//2,g-Ab-m)
   ghi=min(g-1,Aa+m,g-(Ab+3)//2)
   for ga in range(glo,ghi+1):
    gb=g-ga
    lo=max(0,kk-gb+1,2*ga-Aa-m-1)
    hi=min(ga-1,kk,2*ga-2-Aa)
    for ia in range(lo,hi+1):
     ib=kk-ia;r=2*ga-2-Aa-ia
     x=node(ga,ia,aa,r)
     if x:boundary+=(-1)**r*mult*x*node(gb,ib,bb,m-1-r)
  out+=BERN[m]*(v+boundary*HALF)
 return out*INV[k]%P

def J(g,k,ds):
 ds=tuple(ds)
 if k<0 or k>g or sum(ds)+k!=2*g-3+len(ds):return 0
 if g==0:return Q(factorial(len(ds)-3),prod(factorial(d) for d in ds)) if k==0 else 0
 if k==g:return 0
 if k==0:return b(g)*FACT[sum(ds)]*prod(IFACT[d] for d in ds)%P
 if 0 in ds:
  rest=list(ds);rest.remove(0);out=0
  for d,c in Counter(rest).items():
   if d:
    aa=rest.copy();aa.remove(d);aa.append(d-1);out+=c*J(g,k,aa)
  return out%P
 if 1 in ds:
  aa=list(ds);aa.remove(1);return (2*g-3+len(ds))*J(g,k,aa)%P
 return K(g,k,tuple(d-1 for d in ds))
