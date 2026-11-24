import sympy as sp,itertools,pickle,json,os
from pathlib import Path
Path('workspace/agent1_k5_endpoint_verify.py').write_text(Path(__file__).read_text())
from sage.all import PolynomialRing,QQ
k=5;T,c=sp.symbols('T c');xs=sp.symbols('x0:5');us=sp.symbols('u0:5');vs=sp.symbols('y0:5')
cache='workspace/agent1_k5_polarized_poly.pkl'
if os.path.exists(cache):
 with open(cache,'rb')as f:terms=pickle.load(f)
else:
 ps=[T**i*(1-xs[i]*T)*(1-us[i]*T)for i in range(k)]+[(1-c*T)*sp.prod(T+x for x in xs),(T+c)*sp.prod(T+y for y in vs)]
 # Laplace in two last rows, banded minors simple small polys
 Q=sp.Matrix([[sp.Poly(p,T).nth(j)for j in range(k+2)]for p in ps[:k]])
 aa=[sp.Poly(ps[k],T).nth(j)for j in range(k+2)];bb=[sp.Poly(ps[k+1],T).nth(j)for j in range(k+2)]
 D=0
 for i in range(k+2):
  for j in range(i+1,k+2):
   cols=[t for t in range(k+2)if t not in(i,j)]
   D+=(-1)**(i+j+1)*Q[:,cols].det(method='domain-ge')*(aa[i]*bb[j]-aa[j]*bb[i])
 terms=sp.Poly(D,c,*xs,*us,*vs).terms()
 with open(cache,'wb')as f:pickle.dump(terms,f)
print('genericterms',len(terms),flush=True)
R=PolynomialRing(QQ,names=['c']+['x'+str(i)for i in range(k)]);S=PolynomialRing(QQ,names=['v'+str(i)for i in range(k+1)]);ww=S.gens();maps=[]
for j in range(k+1):
 order=list(range(1,j+1))+[0]+list(range(j+1,k+1));mp=[None]*(k+1)
 for t,z in enumerate(order):mp[z]=sum(ww[:t+1])
 maps.append(mp)
results=[]
for ind,bits in enumerate(itertools.product([0,1],repeat=2*k)):
 dct={}
 for pw,co in terms:
  new=list(pw[:k+1])
  for i in range(k):
   new[0 if bits[i] else i+1]+=pw[k+1+i]
   new[0 if bits[k+i] else i+1]+=pw[2*k+1+i]
  tt=tuple(new);dct[tt]=dct.get(tt,0)+int(co)
 p=R(dct)
 for j,mp in enumerate(maps):
  q=p(*mp);coeffs=q.coefficients();neg=sum(1 for a in coeffs if a<0)
  results.append(dict(bits=bits,regime=j,terms=len(coeffs),negative=neg,min=str(min(coeffs))))
  assert neg==0,(bits,j,neg)
 if ind%32==0:print('flags',ind,'checked',len(results),flush=True)
with open('workspace/agent1_k5_endpoints_results.json','w')as f:json.dump(results,f)
print('all',len(results),'positive',flush=True)
