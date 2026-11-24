import sympy as S,json
from pathlib import Path
n,j,D,y,x,t,u=S.symbols('n j D y x t u')
Qs=[S.sympify(q,locals={'n':n,'j':j}) for q in json.loads(Path('workspace/agent3_telescopers.json').read_text())]
MM=[S.factor((n-1)**2*Q.subs(j,0))+S.factor(n*n*Q.subs(j,1))*y for Q in Qs]
def mom(poly):
    return S.factor(sum(c*MM[mon[0]] for mon,c in S.Poly(S.expand(poly),D).terms()))
def radial(ss,kk):
    out=0;aa=(n+1)/2
    if ss in [2,3]:
        for m in range(kk+1):
            out+=(-1)**(kk-m)*S.binomial(kk,m)*S.prod(D+r*(n-r) for r in range(m))/(S.factorial(m+(ss==3))*S.prod(aa-r for r in range(1,m+1)))
    else:
        for m in range(1,kk+1):
            out+=2*(-1)**(kk-m)*S.binomial(kk,m)*S.prod(D+(r+1)*(n-1-r) for r in range(m-1))/(S.factorial(m-1)*S.prod((n-1)/2-r for r in range(1,m)))
    return S.factor(out)
G={}
for ss in [1,2,3]:
    rs=[radial(ss,k) for k in range(3 if ss==3 else 4)]
    fac={1:D/(n-1)**2,2:1,3:D-(n+1)}[ss]
    G[ss]=S.Matrix([[mom(fac*r*q) for q in rs] for r in rs])
    print('built angular',ss,flush=True)
Path('workspace/agent4_symbolic_angular_grams.json').write_text(json.dumps({str(ss):[[str(v) for v in row] for row in G[ss].tolist()] for ss in G}))
a=[1,-S.Rational(2,5),S.Rational(9,200),-S.Rational(9,8000)]
lo=S.Rational(19,20);hi=S.Rational(11,10)
cert=[]
for rho in [(n-2)/(n*(n-1)),n/((n-2)*(n-1))]:
    coefs=[0]*7;dd=n-1
    for k in range(4):
        for l in range(4):
            ck=1+2*k/(dd+2);cl=1+2*l/(dd+2)
            bb=2*(dd+2)*rho*ck*cl*G[1][k,l]
            if k and l:bb+=4*(1/(dd+4)+2*dd*rho/((dd+2)*(dd+4)))*k*l*G[3][k-1,l-1]
            if l:bb+=l*(2+8*rho+4*(l-1)/(dd+4)*(1+4*rho))*G[2][k,l-1]
            coefs[k+l]+=a[k]*a[l]*bb
    coefs=[S.factor(c) for c in coefs]
    B=sum(c*x**k for k,c in enumerate(coefs))
    print('built translation rho=',rho,flush=True)
    # Bernstein on [lo,hi] computed with affine monomial transformation without rational expression expansion.
    transformed=[S.factor(sum(coefs[k]*S.binomial(k,i)*lo**(k-i)*(hi-lo)**i for k in range(i,7))) for i in range(7)]
    bern=[S.factor(sum(transformed[i]*S.binomial(k,i)/S.binomial(6,i) for i in range(k+1))) for k in range(7)]
    for k,b in enumerate(bern):
        for yy in [8/(S.Rational('3.1416')*(n+1)),8/(S.Rational('3.14159')*n)]:
            num,den=S.fraction(S.factor(b.subs(y,yy)))
            pn=S.Poly(S.expand(-num.subs(n,t+20)),t);pd=S.Poly(S.expand(den.subs(n,t+20)),t)
            assert all(v>0 for v in pn.all_coeffs()),(rho,k,yy,'numerator',pn.all_coeffs())
            assert all(v>0 for v in pd.all_coeffs()),(rho,k,yy,'denominator')
            cert.append({'rho':str(rho),'k':k,'yy':str(yy),'negative_numerator_coefficients':[str(v) for v in pn.all_coeffs()]})
        print('checked rho,k',rho,k,flush=True)
Path('workspace/agent4_alln_translation_certificate.json').write_text(json.dumps(cert))
Path('workspace/agent4_alln_translation_checks.py').write_text(Path(__file__).read_text())
print('ALL real n>=20 full translation strictness certified.')
Path('workspace/agent4_highdim_algebra.md').write_text(r'''# Exact algebraic strict-minimum certificate (not a nonlinear PDE theorem)

Let d=n-1 and let H_2(z)=z^T Tz, tr(T)=0. Set
p(s)=1-2s/5+9s^2/200-9s^3/8000 and h(z)=H_2(z)p(|z|^2).
Consider the quadratic shape response Q(h)=<D f,DN^{-1} D f>, where
f=2h/(1+|z|^2), D=Delta_{S^{n-1}}+n-1, and DN is for Delta_{S^n}+n.
The constant/linear graph modes lie in the response kernel.

For boundary spherical harmonic degree L>=2,
mu_L=2 Gamma((L+n+1)/2) Gamma(L/2) /
       (Gamma((L-1)/2) Gamma((L+n)/2)).
This follows by separation with sin(theta)^L times the Gauss hypergeometric function
with parameters ((L-1)/2,(L+n)/2;L+n/2;sin(theta)^2), and continuation at 1.

For angular degree2 write L=j+2, a=(n+1)/2, alpha=(n+2)/2,
and D_L=(L-1)(L+n-1). Its radial coefficient polynomial for r^(2k) is
R2_k(D)=sum_{m=0}^k (-1)^(k-m) binom(k,m)
 prod_{r=0}^{m-1}(D+r(n-r))/(m! prod_{r=1}^m(a-r)).
Up to a common positive constant, its Gram matrix is the moment matrix
G2_kl=sum_{j>=0} W_j R2_k(D_L)R2_l(D_L), where
W_j=(j+alpha)[Gamma((j+3)/2)/Gamma((j+n+1)/2)]^2.
For angular degree3 the corresponding R3_k replaces m! by (m+1)!, and the
weight is (D_L-(n+1))W_j. For angular degree1 (constant graph mode killed),
R1_k(D)=2 sum_{m=1}^k (-1)^(k-m)binom(k,m)
 prod_{r=0}^{m-2}(D+(r+1)(n-1-r)) /
 ((m-1)! prod_{r=1}^{m-1}((n-1)/2-r)),
and the weight is D_L W_j/(n-1)^2.
These equalities follow from Jacobi Rodrigues integration by parts. The
cross-angular constants are included, not discarded.

The moments M_k=sum W_j D_L^k, k<=6, are evaluated by exact telescopers
Q_k(j,n) in agent3_telescopers.json:
(j+n-1)^2 Q_k(j)-(j+3)^2 Q_k(j+2)=(j+alpha)D_L^k.
Thus M_k=(n-1)^2 Q_k(0) Gamma(3/2)^2/Gamma((n+1)/2)^2
+n^2 Q_k(1)/Gamma((n+2)/2)^2. The tail vanishes for n>4+2k.
Consequently all required matrices are exact for n>16. After a common positive
factor is removed, entries are affine in
y=4 Gamma((n+1)/2)^2/(pi Gamma((n+2)/2)^2).
Gamma log-convexity gives 8/[pi(n+1)]<y<8/[pi n].

For x=lambda^2 let a(x)=(1,-2x/5,9x^2/200,-9x^3/8000).
The scale shape response is q(x)=x a(x)^T G2 a(x).
Agent3_alln_scale_check.py and agent3_alln_scale_strict_check.py prove exactly,
for every real n>=20, q'(.95)>0, q'(1.1)<0, and q''<0 on this interval.
Hence a unique strict scale maximum exists there.

For a T eigenvalue tau define rho=tau^2/tr(T^2). The translation Hessian
bracket is a(x)^T B_rho a(x), with d=n-1, c_k=1+2k/(d+2), and
B_kl=2(d+2)rho c_k c_l G1_kl
 +4[1/(d+4)+2d rho/((d+2)(d+4))]kl G3_(k-1,l-1)
 +l[2+8rho+4(1+4rho)(l-1)/(d+4)]G2_(k,l-1),
where absent negative indices give zero and B is symmetrized.
Agent4_alln_translation_checks.py proves this bracket strictly negative on
x in [.95,1.1], n>=20, and
rho in [(n-2)/(n(n-1)), n/((n-2)(n-1))].
It checks the two rho endpoints and two gamma-ratio endpoints. Each of the
seven Bernstein coefficients has, after sign reversal, a numerator and
denominator with strictly positive coefficients in n-20. This is an exact
finite polynomial certificate for all real n>=20, not a dimension scan.

Choose T diagonal: q repeated p times, -p repeated q times, where
p=floor(d/2), q=d-p. The two rho values belong to the certified interval.
Coordinate reflection symmetries force the translation gradient and all
mixed Hessians to vanish. Thus -Q has a strict full scale/translation
minimum in this quadratic model for every integer n>=20.

IMPORTANT LIMITATION: this proves only the quadratic finite-dimensional
algebra. A separate uniform Lyapunov-Schmidt construction and fixed-domain
iteration are needed to produce solutions. Moreover the same model admits
a rigorously certified strict minimum in dimension19 (agent3 certificate),
so it cannot be used as a proof of the requested dimension19 compactness.
''')
