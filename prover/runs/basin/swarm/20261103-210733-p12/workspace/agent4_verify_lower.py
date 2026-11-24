"""Reproducible lower-bound verifier (Python + Sage + SymPy).
Run after agent2_verify_support.py, from the directory containing workspace/.
  python workspace/agent4_verify_lower.py
  python workspace/agent4_verify_lower.py --recompute-roots
The second command recomputes every genus25 Hodge root from Mumford-GRR /
Newton recursion; it can take hours from a cold cache. No FZ-completeness or
Gorenstein hypothesis is used. The default checks the already computed roots,
recomputes the 1574-term aggregation and all twelve boundary integrals from
the EXACT rational supported-Q certificates.
"""
import sys,json,pickle,time,glob,runpy
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from collections import Counter
from itertools import product
from math import comb,factorial
sys.path.insert(0,'workspace')
from sage.all import GF,bernoulli
from agent4_pairing import P,partitions,intersection
F=GF(P)

@lru_cache(None)
def splits(a):
 c=Counter(a);ks=tuple(c);cs=tuple(c[k] for k in ks);out=[]
 for vv in product(*(range(v+1) for v in cs)):
  x=tuple(sorted((k for k,v in zip(ks,vv) for _ in range(v)),reverse=True))
  y=tuple(sorted((k for k,c0,v in zip(ks,cs,vv) for _ in range(c0-v)),reverse=True))
  z=1
  for c0,v in zip(cs,vv):z*=comb(c0,v)
  out.append((x,y,z))
 return out

@lru_cache(None)
def point(a,t,g):
 # Raw integral on Mbar_g,1 with logarithmic kappa. Multiply by T_g below.
 assert sum(a)+t==g-1
 out=0
 for x,y,z in splits(a):
  s=t+sum(y)
  if s==0:continue
  k=s-1
  if k==0:v=(2*g-2)*intersection(x,g)
  else:v=intersection(tuple(sorted(x+(k,),reverse=True)),g)
  out+=z*v
 return out%P

@lru_cache(None)
def factor(h,d):
 return pickle.load(open('workspace/agent2_exactfactor_%02d_%02d.pkl'%(h,d),'rb'))

def boundary(E):
 def value(g,h,x,y):
  I,t=x;J,u=y;out=0
  for p,c in E:
   v=0
   for a,b,z in splits(p):
    if sum(a)+sum(I)+t!=g-1:continue
    va=1 if g==1 else point(tuple(sorted(a+I,reverse=True)),t,g)
    v+=z*va*point(tuple(sorted(b+J,reverse=True)),u,h)
   out+=c*(v%P)
  return out%P
 T=lambda k:F(abs(bernoulli(2*k)))/F(2**(2*k-1)*factorial(2*k))
 total=F(0);vals=[]
 for g in range(1,13):
  h=25-g;cert=pickle.load(open('workspace/agent2_exact_divisibility_%02d.pkl'%g,'rb'))
  assert cert['M']*cert['solution']==cert['target']
  ans=F(0)
  for v,(d,x,y) in zip(cert['solution'],cert['domain']):
   if not v:continue
   a=factor(g,d);b=factor(h,11-d)
   xx=a['basis'][a['free'][x]];yy=b['basis'][b['free'][y]]
   ans+=F(v)*value(g,h,xx,yy)
  ans*=T(g)*T(h);total+=ans;vals.append(int(ans))
 return int(total),vals

def roots():
 values={}
 files=['agent4_J0_500.json','agent1_J500_1000.json',
 'agent1_Joriginal500_1000.json','agent3_J1000_1250.json',
 'agent2_J1250_1575.json','agent4_J1400_1575.json',
 'agent1_J1200_1250.json','agent1_J1450_1500.json','agent3_J1500_1575.json']
 for name in files:
  path=Path('workspace')/name
  if not path.exists():continue
  for i,v in json.load(open(path)).items():
   i=int(i);v=int(v)
   if i in values:assert values[i]==v,(name,i)
   values[i]=v
 return values

def main():
 import sympy as sp
 from sympy.polys.matrices import DomainMatrix
 # Recompute all standard intersections rationally and exhibit the exceptional class.
 runpy.run_path('workspace/agent4_pairing_exact.py',run_name='__main__')
 data=json.load(open('workspace/agent4_pairing_exact.json'))
 basis=[tuple(v) for v in data['basis12']]
 M=sp.Matrix([[sp.Rational(v) for v in row] for row in data['matrix']])
 assert DomainMatrix.from_Matrix(M).rank()==43
 ed=json.load(open('workspace/fz25_exceptional.json'))
 E=[(tuple(a),int(c)) for a,c in zip(ed['basis'],ed['vector'])]
 e=sp.zeros(77,1)
 for a,c in E:e[basis.index(a)]=c
 assert M.T*e==sp.zeros(56,1)
 fz=json.load(open('workspace/fz25_upper_data.json'))
 assert fz['basis']==data['basis12']
 R=sp.Matrix([[sp.Rational(c) for c in row] for row in fz['matrix']])
 assert R*M==sp.zeros(59,56)
 assert DomainMatrix.from_Matrix(R.col_join(e.T)).rank()==34
 print('Standard rank43 and exceptional non-FZ class checked exactly.',flush=True)
 # Recompute psi-pushforward expansion of Pgood times E; never trust aggregate data.
 import agent1_hodge_mod as H
 pd=json.load(open('workspace/agent2_Pgood.json'))
 W=Counter()
 for a,c in pd['terms']:
  cc=H.Q(Fraction(c))
  for b,d in E:
   for p,z in H.kappa_expansion(tuple(sorted(tuple(a)+b))):
    W[p]=(W[p]+cc*d*z)%P
 W={a:c for a,c in W.items() if c}
 assert len(W)==1574
 ps=list(partitions(24));idx={a:i for i,a in enumerate(ps)}
 values=roots()
 if '--recompute-roots' in sys.argv:
  import agent1_Kpersist as K
  K.CACHE_FILE='workspace/lower_verifier_Kcache.pkl'
  for j,a in enumerate(W):
   i=idx[tuple(sorted(a,reverse=True))]
   v=int(K.J(25,23,tuple(x+1 for x in a)))
   if i in values:assert values[i]==v,(i,v,values[i])
   values[i]=v
   if j%20==0:K.save();print('Recomputed Hodge roots',j,len(W),flush=True)
  K.save()
 missing=[idx[tuple(sorted(a,reverse=True))] for a in W if idx[tuple(sorted(a,reverse=True))] not in values]
 assert not missing,missing
 bulk=sum(c*values[idx[tuple(sorted(a,reverse=True))]] for a,c in W.items())%P
 bnd,contributions=boundary([(a,c%P) for a,c in E])
 total=(bulk+bnd)%P
 print('Bulk',bulk,'boundary',bnd,'corrected',total,flush=True)
 assert bnd==296879567
 assert bulk==799683810
 assert total==96563370 and total!=0
 print('VERIFIED: 43 standard functionals plus one independent supported Hodge functional give dimension at least44.')
if __name__=='__main__':main()
