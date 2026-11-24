import sympy as S,numpy as np,scipy.linalg as la
from pathlib import Path
x=S.symbols('x')
def translation_model(n,d):
 a=S.Rational(n,2);q=x*x-a*a
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
 def t2(h):return S.prod(x*x-(a-r)**2 for r in range(h))/(S.factorial(h)*S.prod(2*a+1-2*r for r in range(1,h+1)))
 R2=[S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*t2(h)for h in range(j+1)))for j in range(d+1)]
 def t3(h):return S.prod(x*x-(a+1-r)**2 for r in range(h+1))/(S.factorial(h+1)*S.prod(2*a+3-2*r for r in range(1,h+2)))
 R3=[S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*t3(h)for h in range(j+1)))for j in range(d)]
 def t1(h):return S.prod(x*x-(a-1-r)**2 for r in range(h-1))/(S.factorial(h-1)*S.prod(2*a-1-2*r for r in range(1,h)))
 R1=[S.expand(sum(S.binomial(j,h)*2**h*(-1)**(j-h)*t1(h)for h in range(1,j+1)))for j in range(d+1)]
 G2=S.Matrix(d+1,d+1,lambda i,j:moment(R2[i]*R2[j]))
 G1=S.Matrix(d+1,d+1,lambda i,j:moment(q*R1[i]*R1[j])/(n-1)**2)
 G3=S.Matrix(d,d,lambda i,j:(n+1)**2*moment(S.cancel(R3[i]*R3[j]/(x*x-(a+1)**2))))
 N2=np.array(G2.evalf(),float);N1=np.array(G1.evalf(),float);N3=np.array(G3.evalf(),float)
 powers=np.array([[2+2*i+2*j for j in range(d+1)]for i in range(d+1)])
 ev,vc=la.eigh(N2*powers,N2);v=vc[:,0]/vc[0,0]
 cp=np.zeros(2*d+1)
 for i in range(d+1):
  for j in range(d+1):cp[i+j]+=powers[i,j]*N2[i,j]*v[i]*v[j]
 roots=np.polynomial.polynomial.polyroots(cp);roots=sorted(z.real for z in roots if abs(z.imag)<1e-6 and z.real>0)
 print('n,d',n,d,'eig',ev,'v',v,'roots',roots)
 for t in roots:
  aa=v*t**np.arange(d+1);m=n-1
  g=aa*(1+2*np.arange(d+1)/(m+2))
  b=np.array([2*(j+1)*aa[j+1] for j in range(d)])
  c=np.zeros(d+1);c[:d]=[2*(j+1)*(1+2*j/(m+4))*aa[j+1]for j in range(d)]
  PN=4/(m*(m+2));C=PN*aa@N2@c
  H1=2*(4/m*(g@N1@g)+8*(m+1)/(m*(m+2)**2*(m+4))*(b@N3@b)+3*C)
  H3=2*(4/(m*(m+2)*(m+4))*(b@N3@b)+C)
  Hs=aa@(N2*powers*(powers-1))@aa
  print('root,Hnorm supported,transverse,scale:',t,H1,H3,Hs)
 return G1,G2,G3
if __name__=='__main__':
 for n,d in [(19,3),(20,3),(21,2)]:translation_model(n,d)
