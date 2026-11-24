import sympy as s
from pathlib import Path
import time,json
n,z=s.symbols('n z');a=(n-4)/2;k=z-(n+2)/2
L=[]
for r in range(7):L.append(s.Poly(s.expand((z+a)**2*(z-1)**(2*r)-(z-a)**2*(z+1)**(2*r)),z))
E0=[];E1=[]
for r in range(7):
 b=[s.Integer(0)]*(r+1)
 for j in range(r,-1,-1):
  v=4*a if j==r else s.Integer(0)
  for h in range(j+1,r+1):v-=b[h]*L[h].coeff_monomial(z**(2*j+1))
  b[j]=s.factor(v/L[j].coeff_monomial(z**(2*j+1)))
 for power in range(2*r+2):
  assert s.factor(sum(b[j]*L[j].coeff_monomial(z**power) for j in range(r+1))-(4*a if power==2*r+1 else 0))==0
 E0.append(s.factor(sum(b[j]*(n/2)**(2*j) for j in range(r+1))))
 E1.append(s.factor(sum(b[j]*(n/2+1)**(2*j) for j in range(r+1))))
 print('monomial',r,'done',flush=True)
G=[]
for i in range(4):
 v=0
 for j in range(i+1):
  R=s.prod(k+h for h in range(1,j+1))*s.prod(k+n+3-(j+1)+h for h in range(j))/(s.factorial(j)*s.prod(n+1-2*h for h in range(1,j+1)))
  v+=s.binomial(i,j)*2**j*(-1)**(i-j)*R
 P=s.Poly(s.expand(v),z)
 assert all(P.coeff_monomial(z**h)==0 for h in range(1,2*i+1,2))
 G.append(P)
A=s.zeros(4);B=s.zeros(4)
for i in range(4):
 for j in range(i,4):
  P=G[i]*G[j]
  aa=s.factor(sum(P.coeff_monomial(z**(2*r))*E0[r] for r in range(i+j+1)))
  bb=s.factor(sum(P.coeff_monomial(z**(2*r))*E1[r] for r in range(i+j+1)))
  A[i,j]=A[j,i]=aa;B[i,j]=B[j,i]=bb
  print('entry',i,j,'done',flush=True)
Path('workspace/agent4_symbolic_M_AB.txt').write_text('A='+str(A)+'\nB='+str(B)+'\n')
import pickle
with open('workspace/agent4_symbolic_M_AB.pkl','wb') as f:pickle.dump((n,A,B),f)
for nn in [17,18,19,20,30,100]:
 import numpy as np
 t=4*s.gamma(s.Rational(nn-1,2))**2/(s.pi*s.gamma(s.Rational(nn,2))**2)
 M=np.array((A+t*B).subs(n,nn)).astype(float)
 K=M*(1+np.arange(4)[:,None]+np.arange(4)[None,:]);scale=np.sqrt(np.diag(K))
 print('n',nn,'eigs',np.linalg.eigvalsh(K/scale[:,None]/scale[None,:]))
Path('workspace/agent4_symbolic_M_checks.py').write_text(Path(__file__).read_text())
