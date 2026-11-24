"""Exact residue verification of an explicit neutral-kernel left witness.
For full-real negative-level roots, choose monic W with a root in each
negative-level pair; alpha_j=h(z_j)W(z_j)/(QP+1)'(z_j)>0 then C^Talpha>0.
The algebra below checks the root-free identity also for complex roots;
it does NOT prove positivity when some negative-level roots are nonreal.
"""
import sympy as S

def check(s):
 z=S.symbols('z')
 Q=z**s+sum(S.Rational(j+1,2*s+3)*z**j for j in range(s))
 P=z**s+sum(S.Rational((-1)**j*(j+2),3*s+5)*z**j for j in range(s))
 h=z**(s-1)+sum(S.Rational(j+1,5*s+7)*z**j for j in range(s-1))
 Rp=S.Poly(S.expand(Q*P-1),z);Rn=S.Poly(S.expand(Q*P+1),z)
 def residues(num,den):
  rem=S.rem(S.Poly(S.expand(num),z),den)
  return rem.nth(den.degree()-1)/den.LC()
 def L(num):return residues(P*h*num,Rp)
 G=S.Matrix(s+1,s+1,lambda i,j:L(z**(i+j)))
 H=S.Matrix(s+1,s+1,lambda i,j:L(Q**2*z**(i+j)))
 q=S.Matrix([S.expand(Q).coeff(z,j) for j in range(s+1)])
 p=S.Matrix([S.expand(P).coeff(z,j) for j in range(s+1)])
 e=S.zeros(s+1,1);e[s]=1
 assert G*q==H*p==e
 for degree in range(s+1):
  W=z**degree
  u=S.Matrix([-residues(P*h*W*z**j,Rn) for j in range(s+1)])
  v=S.Matrix([residues(Q*h*W*z**j,Rn) for j in range(s+1)])
  A=G.inv()*u;B=H.inv()*v
  Avec=sum(A[j]*z**j for j in range(s+1));Bvec=sum(B[j]*z**j for j in range(s+1))
  expected=2*(Q-P) if degree==s else 0
  assert S.expand(Avec+Bvec-expected)==0
  cta=S.rem(S.Poly(S.expand(Q*(Avec+Bvec)),z),Rn)
  exp=S.rem(S.Poly(S.expand(2*(Q**2+1) if degree==s else 0),z),Rn)
  assert cta==exp

if __name__=='__main__':
 for s in range(1,6):check(s)
 print('Exact neutral left-witness residue identities passed for s=1,...,5.')
