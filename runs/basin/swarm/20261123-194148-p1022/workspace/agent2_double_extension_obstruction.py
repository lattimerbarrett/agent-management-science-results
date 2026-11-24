import sys
sys.path.insert(0,'workspace')
import sympy as s
from agent4_chern_constraints import x,y,schur,reduce_xy
from agent1_chern_eliminate import eliminate

def chern_constraints(ranks,weights,target):
 coeffs=[s.Integer(1)];vs=[]
 for i,(r,w) in enumerate(zip(ranks,weights)):
  C=[s.Integer(1)]
  for j in range(1,r+1):
   c=0
   for a in range(4):
    b=j-a
    if 0<=b<=a:
     v=s.Symbol(f'c{i}_{a}{b}');vs.append(v);c+=v*schur(a,b)
   C.append(c)
  D=[0]*(r+1)
  for j,c in enumerate(C):
   for k in range(r-j+1):D[j+k]+=s.binomial(r-j,k)*(w*x)**k*c
  new=[0]*(len(coeffs)+r)
  for j,a in enumerate(coeffs):
   for k,b in enumerate(D):new[j+k]+=a*b
  coeffs=[reduce_xy(c) for c in new]
 eq=[]
 for k,c in enumerate(coeffs):
  c-=target[k]*x**k if k<len(target) else 0
  for mon,v in s.Poly(c,x,y).terms():
   if v!=0:eq.append(v)
 eq,vs,sub=eliminate(eq,vs)
 print('remaining',len(vs),len(eq),vs,flush=True)
 if vs:
  gb=s.groebner(eq,*vs,order='grevlex');print(list(gb),flush=True);return list(gb)
 print(eq)

chern_constraints((1,5,1),(0,1,2),[1,7,22,40,40])
