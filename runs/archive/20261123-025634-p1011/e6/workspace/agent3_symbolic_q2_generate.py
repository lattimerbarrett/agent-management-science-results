import sympy as s
from pathlib import Path
k,n=s.symbols('k n')
W=[]
for i in range(4):
 v=0
 for j in range(i+1):
  ratio=s.rf(k+1,j)*s.rf(k+n-j+2,j)/(s.factorial(j)*s.prod(n+1-2*r for r in range(1,j+1)))
  v+=s.binomial(i,j)*2**j*(-1)**(i-j)*ratio
 W.append(s.Poly(s.expand(v),k))
def Q(w):
 H=s.Poly(s.expand((2*k+n+2)*w.as_expr()),k);D=H.degree()-1
 out=0
 for j in range(D,-1,-1):
  op=s.Poly(s.expand((k+n-1)**2*k**j-(k+3)**2*(k+2)**j),k)
  c=s.factor(H.nth(j+1)/(2*(n-4-j)))
  out+=c*k**j
  H=s.Poly.from_dict({(d,):s.factor(H.nth(d)-c*op.nth(d)) for d in range(j+2)},k)
 assert all(s.factor(c)==0 for c in H.all_coeffs()),H
 return s.Poly(out,k)
res={}
for i in range(4):
 for j in range(i,4):
  q=Q(W[i]*W[j]);q0=s.factor(q.eval(0));q1=s.factor(q.eval(1))
  res[i,j]=(q0,q1)
  print(i,j,'done',flush=True)
import pickle
with open('workspace/agent3_symbolic_q2.pkl','wb') as f:pickle.dump(res,f)
Path('workspace/agent3_symbolic_q2.txt').write_text('\n'.join(f'{i},{j}: Q0={u}; Q1={v}' for (i,j),(u,v) in res.items()))
