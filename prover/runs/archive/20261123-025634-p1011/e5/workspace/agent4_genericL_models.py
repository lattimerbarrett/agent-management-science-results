import sympy as S,numpy as np,scipy.linalg as la,json
from pathlib import Path
x=S.symbols('x')
def gram(n,L,d):
 a=S.Rational(n,2);alpha=a+L-1;q=x*x-a*a
 def anti(F):
  rem=S.Poly(S.expand(F),x);P=S.S.Zero
  if rem.is_zero:return P
  for k in range((rem.degree()-1)//2,-1,-1):
   c=rem.coeff_monomial(x**(2*k+1))/(4*(a-k));P+=c*x**(2*k)
   rem-=S.Poly(S.expand(c*((x+a)**2*(x-1)**(2*k)-(x-a)**2*(x+1)**(2*k))),x)
  assert rem.is_zero
  return P
 def moment(F):
  P=anti(x*q*q*S.cancel(F))
  return S.factor((2*a+1)**2*S.pi*P.subs(x,a)/S.gamma(a+S.Rational(3,2))**2+(2*a+2)**2*P.subs(x,a+1)/S.gamma(a+2)**2)
 def T(s):
  assert s>=1
  return S.prod(x*x-(alpha-1-r)**2 for r in range(s-1))/(S.factorial(s-1)*S.prod(2*alpha-2*r-1 for r in range(1,s)))
 R=[]
 for j in range(d+1):
  R.append(S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*T(L+h-1)for h in range(max(0,2-L),j+1))))
 if L>=2:
  den=S.prod(x*x-(a+1+r)**2 for r in range(L-2));fac=S.prod((n+1+2*r)**2 for r in range(L-2))
  E=lambda i,j:fac*S.cancel(R[i]*R[j]/den)
 elif L==1:E=lambda i,j:q*R[i]*R[j]/(n-1)**2
 else:E=lambda i,j:q*(x*x-(a-1)**2)*R[i]*R[j]/((n-3)**2*(n-1)**2)
 active=list(range(max(0,2-L),d+1))
 G=S.Matrix(len(active),len(active),lambda i,j:moment(E(active[i],active[j])))
 D=S.Matrix(len(active),len(active),lambda i,j:(2*L+2*active[i]+2*active[j]-2)*G[i,j])
 return active,G,D
if __name__=='__main__':
 result=[]
 for n in range(9,26):
  row=[]
  for L in range(0,7):
   d=min(4,(n-2*L-1)//4)
   if d<max(0,2-L):continue
   active,G,D=gram(n,L,d)
   ev=la.eigvalsh(np.array(D.evalf(),float),np.array(G.evalf(),float))
   row.append((L,d,float(ev[0])))
  print(n,row);result.append({'n':n,'models':row})
 Path('workspace/agent4_genericL_results.json').write_text(json.dumps(result,indent=2))
 import shutil,os
 if os.path.abspath(__file__)!=os.path.abspath('workspace/agent4_genericL_models.py'):shutil.copyfile(__file__,'workspace/agent4_genericL_models.py')
