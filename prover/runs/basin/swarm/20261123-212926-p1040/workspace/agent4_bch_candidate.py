from fractions import Fraction as F
from functools import lru_cache
from math import factorial
from collections import defaultdict
import json,pickle,time
from pathlib import Path
D=8

def add(a,b,s=1):
 a=a.copy()
 for w,v in b.items():
  z=a.get(w,0)+s*v
  if z:a[w]=z
  elif w in a:del a[w]
 return a

def mul(a,b,degree=D):
 out=defaultdict(F)
 aa=defaultdict(list);bb=defaultdict(list)
 for w,v in a.items():aa[len(w)].append((w,v))
 for w,v in b.items():bb[len(w)].append((w,v))
 for i,terms in aa.items():
  for j,terms2 in bb.items():
   if i+j>degree:continue
   for w,v in terms:
    for x,t in terms2:out[w+x]+=v*t
 return {w:v for w,v in out.items() if v}

def inv(a,degree=D): # inverse of 1+a
 out={():F(1)};term={():F(1)}
 if not a:return out
 for k in range(degree//min(map(len,a))+1):
  term=mul(term,a,degree)
  if not term:break
  out=add(out,term,(-1)**(k+1))
 return out

def lyndon(w):return all(w<w[i:] for i in range(1,len(w)))
def split(w):
 for i in range(1,len(w)):
  if lyndon(w[i:]):return w[:i],w[i:]
@lru_cache(None)
def comm(w): # standard Lyndon group commutator in exp(letter), minus 1
 if len(w)==1:return {w*k:F(1,factorial(k)) for k in range(1,D+1)}
 u,v=split(w);a=comm(u);b=comm(v)
 delta=add(mul(a,b),mul(b,a),-1)
 return mul(mul(delta,inv(a,D-len(w))),inv(b,D-len(w)))
@lru_cache(None)
def lie(w):
 if len(w)==1:return {w:F(1)}
 u,v=split(w);return add(mul(lie(u),lie(v)),mul(lie(v),lie(u)),-1)

def decompose(poly):
 out={};a=poly.copy()
 while a:
  w=min(a)
  assert lyndon(w),(w,a[w])
  c=a[w];out[w]=c;a=add(a,lie(w),-c)
 return out

if __name__=='__main__':
 base=Path(__file__).parent
 rel=json.loads((base/'agent4_mccool_degree6_relation.json').read_text())
 g={}
 for r in rel:
  assert not r['inner']
  g=add(g,comm(tuple(r['word'])),F(r['coefficient']))
 print('g components',{d:sum(len(w)==d for w in g) for d in range(6,9)},flush=True)
 p7={w:v*2 for w,v in g.items() if len(w)==7}
 c7=decompose(p7)
 assert all(v.denominator==1 for v in c7.values())
 print('correction terms',len(c7),'max',max(map(abs,c7.values())),flush=True)
 h={w:v*2 for w,v in g.items() if len(w)==8}
 for w,v in c7.items():h=add(h,{z:t for z,t in comm(w).items() if len(z)==8},-v)
 # h8 is logarithm of g^2 times correction group commutators.
 assert all(len(w)==8 for w in h)
 print('h8 terms',len(h),'denominators',sorted(set(v.denominator for v in h.values())),flush=True)
 with (base/'agent4_bch_candidate.pkl').open('wb') as f:pickle.dump((c7,h),f)
