import sympy as s,pickle
from pathlib import Path
k,n=s.symbols('k n');t=s.symbols('t')

def solveQ(target,B,C):
 H=s.Poly(s.expand(target),k);D=H.degree()-1;out=0
 for j in range(D,-1,-1):
  op=s.Poly(s.expand((k+C)**2*k**j-(k+B)**2*(k+2)**j),k)
  c=s.factor(H.nth(j+1)/(2*(C-B-j)))
  out+=c*k**j
  H=s.Poly.from_dict({(d,):s.factor(H.nth(d)-c*op.nth(d)) for d in range(j+2)},k)
 assert all(s.factor(c)==0 for c in H.all_coeffs()),H
 return s.Poly(out,k)

matrices={}
for q in [1,3]:
 W=[]
 ids=list(range(1,4)) if q==1 else list(range(3))
 for i in ids:
  v=0
  for j in range(i+1):
   if q==1:
    if j==0:continue
    ratio=s.rf(k+1,j-1)*s.rf(k+n-j+1,j-1)/(s.factorial(j-1)*s.prod(n-1-2*r for r in range(1,j)))
   else:
    ratio=s.rf(k+2,j)*s.rf(k+n+3-j,j)/(s.factorial(j+1)*s.prod(n+1-2*r for r in range(1,j+1)))
   v+=s.binomial(i,j)*2**j*(-1)**(i-j)*ratio
  W.append(s.Poly(s.expand(v),k))
 out={}
 for i in range(3):
  for j in range(i,3):
   if q==1:
    target=s.expand((2*k+n)*k**3*(k+n)*(W[i]*W[j]).as_expr())
    Q=solveQ(target,0,n-2)
    value=(Q.eval(1)+t*Q.eval(2)/4)/(n-1)**2
   else:
    target=s.expand((2*k+n+4)*(k+1)*(k+2)**2*(k+n+2)**2*(k+n+3)*(W[i]*W[j]).as_expr())
    Q=solveQ(target,2,n+2)
    value=t*Q.eval(0)/(4*n**2)+Q.eval(1)/((n+1)**2*(n-1)**2)
   out[i,j]=s.factor(value)
   print(q,ids[i],ids[j],'done',flush=True)
 matrices[q]=out
with open('workspace/agent3_symbolic_trans_M.pkl','wb') as f:pickle.dump(matrices,f)
Path('workspace/agent3_symbolic_trans_M.txt').write_text('\n'.join(f'q{q} {ij}: {v}' for q,mat in matrices.items() for ij,v in mat.items()))
