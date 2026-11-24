import sympy as S, numpy as np, math, json, pathlib
x=S.symbols('x'); n=21;a=S.Rational(n,2);q=x*x-a*a

def anti(F):
    rem=S.Poly(S.expand(F),x);m=(rem.degree()-1)//2;P=S.S.Zero
    for k in range(m,-1,-1):
        coef=rem.coeff_monomial(x**(2*k+1))/(4*(a-k))
        P+=coef*x**(2*k)
        rem-=S.Poly(S.expand(coef*((x+a)**2*(x-1)**(2*k)-(x-a)**2*(x+1)**(2*k))),x)
    assert rem.is_zero
    return P

R=[]
for j in range(5):
    Rj=0
    for h in range(j+1):
        T=S.prod(x*x-(a-r)**2 for r in range(h))/(S.factorial(h)*S.prod(2*a+1-2*r for r in range(1,h+1)))
        Rj+=S.binomial(j,h)*2**h*(-1)**(j-h)*T
    R.append(S.expand(Rj))
# Independently verify Rodrigues/Gegenbauer moment formula by exact polynomial integration.
t=S.symbols('t');alpha=a+1
K=2**(2*alpha-1)*S.factorial(10)*S.factorial(11)/S.factorial(22)
for ell in range(17):
 for j in range(5):
    poly=S.Poly(S.expand((1+t)**(11+j)*(1-t)**(10-j)*S.gegenbauer(ell,alpha,t)),t)
    exact=sum(co*S.Rational(2,powr[0]+1) for powr,co in poly.terms() if powr[0]%2==0)
    assert S.cancel(exact/K-R[j].subs(x,ell+a+1))==0
print('85 exact Gegenbauer moment identities checked')
# Gram = Mpi*pi + Minvpi/pi. Common positive prefactor omitted.
Mpi=S.zeros(5);Minvpi=S.zeros(5)
for i in range(5):
 for j in range(i,5):
    P=anti(x*q*q*R[i]*R[j])
    A=S.factor((2*a+1)**2*P.subs(x,a)/S.gamma(a+S.Rational(3,2))**2)
    B=S.factor((2*a+2)**2*P.subs(x,a+1)*S.pi/S.gamma(a+2)**2)
    assert A.is_Rational and B.is_Rational
    Mpi[i,j]=Mpi[j,i]=A;Minvpi[i,j]=Minvpi[j,i]=B
G=np.array((Mpi*S.pi+Minvpi/S.pi).evalf(),float)
D=np.array([[(2+2*i+2*j)*G[i,j] for j in range(5)]for i in range(5)])
import scipy.linalg as la
vls,vcs=la.eigh(D,G)
print('degree2 eigen',la.eigh(D[:3,:3],G[:3,:3]))
v=vcs[:,0];v=v/np.max(np.abs(v));print('eigenvalues',vls,'vector',v)
vq=S.Matrix([S.Integer(1),-S.Rational(23,50),S.Rational(6,125),S.Integer(0),S.Integer(0)])
A=S.factor(sum(vq[i]*vq[j]*(2+2*i+2*j)*Mpi[i,j]for i in range(5)for j in range(5)))
B=S.factor(sum(vq[i]*vq[j]*(2+2*i+2*j)*Minvpi[i,j]for i in range(5)for j in range(5)))
# Machin identity gives rigorous pi bounds via alternating Taylor remainder.
def atan_bounds(inv,N=40):
    z=S.Rational(1,inv)
    s=sum((-1)**k*z**(2*k+1)/S.Integer(2*k+1)for k in range(N))
    nxt=(-1)**N*z**(2*N+1)/S.Integer(2*N+1)
    return min(s,s+nxt),max(s,s+nxt)
l5,u5=atan_bounds(5);l239,u239=atan_bounds(239)
lo=16*l5-4*u239;hi=16*u5-4*l239
# pi times quadratic form = A*pi^2+B
lower=A*(lo*lo if A>=0 else hi*hi)+B
upper=A*(hi*hi if A>=0 else lo*lo)+B
assert upper<0
print('rational negative certificate vector',list(vq))
print('A*pi^2+B approximately',float((A*S.pi**2+B).evalf()))
print('relative',float((vq.T*S.Matrix(D)*vq)[0]/(vq.T*S.Matrix(G)*vq)[0]))
print('exact interval upper < 0 verified')
pathlib.Path('workspace/agent4_n21_certificate.json').write_text(json.dumps({'n':n,'vector':[str(z)for z in vq],'A':str(A),'B':str(B),'negative_upper_bound':str(upper),'G_pi':[[str(Mpi[i,j])for j in range(5)]for i in range(5)],'G_invpi':[[str(Minvpi[i,j])for j in range(5)]for i in range(5)]},indent=2))
