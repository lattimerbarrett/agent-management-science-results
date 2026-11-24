import sympy as s
from pathlib import Path
code=r'''import sympy as s
m,k=s.symbols('m k')
def matrix(n,d=3):
    beta=s.Rational(n+1,2);alpha=s.Rational(n+2,2)
    Ps=[]
    for j in range(d+1):
        val=0
        for q in range(j+1):
            T=s.rf(m+n+2-q,q)*s.prod(m+t for t in range(1,q+1))/s.factorial(q)/s.prod(beta-t for t in range(1,q+1))
            val+=(-1)**(j-q)*s.binomial(j,q)*T
        Ps.append(s.expand(val))
    def telescope(P,p):
        b=s.Rational(p+3,2);c=s.Rational(p+n+1,2)
        target=s.Poly(s.expand((2*k+p+alpha)*P.subs(m,2*k+p)),k)
        D=s.degree(P,m)
        rem=target.as_expr();A=0
        for v in range(D,-1,-1):
            L=s.expand((k+c-1)**2*k**v-(k+b)**2*(k+1)**v)
            lc=L.coeff(k,v+1)
            av=s.expand(rem).coeff(k,v+1)/lc
            A+=av*k**v; rem=s.expand(rem-av*L)
        assert rem==0
        return 16*s.gamma(b)**2/s.gamma(c-1)**2*s.expand(A).coeff(k,0)
    Q=s.zeros(d+1)
    for i in range(d+1):
        for j in range(i,d+1):
            P=s.expand(Ps[i]*Ps[j])
            Q[i,j]=Q[j,i]=s.simplify(telescope(P,0)+telescope(P,1))
    return Q
if __name__=='__main__':
    import numpy as np
    for n in (17,18,19,20):
        Q=matrix(n)
        M=s.Matrix(4,4,lambda i,j:(i+j+1)*Q[i,j])
        qa=np.array(Q.evalf(),dtype=float)
        ma=np.array(M.evalf(),dtype=float)
        scale=np.sqrt(np.diag(ma)); normalized=ma/scale[:,None]/scale[None,:]
        print(n,np.linalg.eigvalsh(normalized),flush=True)
        print('det signs', [s.sign(s.N(M[:j,:j].det(),30)) for j in range(1,5)],flush=True)
        s.polys # loaded
        open('workspace/agent4_Q_'+str(n)+'.txt','w').write(str(Q))
'''
Path('workspace/agent4_exact_sums.py').write_text(code)
# exact-sum module saved; run interval certificate below
import sys
sys.path.insert(0,'workspace')
from agent4_exact_sums import matrix
x=s.symbols('x')
def atan_interval(q,N=60):
    v=sum((-1)**j*s.Rational(1,q)**(2*j+1)/s.Integer(2*j+1) for j in range(N))
    w=v+(-1)**N*s.Rational(1,q)**(2*N+1)/s.Integer(2*N+1)
    return min(v,w),max(v,w)
a,b=atan_interval(5);c,d=atan_interval(239)
pl,pu=16*a-4*d,16*b-4*c
assert pl>3 and pu<4

def polynomial_interval(expr):
    poly=s.Poly(s.expand(expr),s.pi)
    lo=hi=s.Rational(0)
    for (power,),coeff in poly.terms():
        if coeff>=0:lo+=coeff*pl**power;hi+=coeff*pu**power
        else:lo+=coeff*pu**power;hi+=coeff*pl**power
    return lo,hi
for n in (17,18,19,20):
    Q=matrix(n);M=s.Matrix(4,4,lambda i,j:(i+j+1)*Q[i,j])
    signs=[]
    for j in range(1,5):
        det=s.factor(M[:j,:j].det())
        # Clear positive powers of pi from denominator; all gamma values already explicit.
        numer,denom=s.fraction(det)
        dl,du=polynomial_interval(denom);assert dl>0
        lo,hi=polynomial_interval(numer)
        assert lo>0 or hi<0
        signs.append(1 if lo>0 else -1)
    print('RIGOROUS principal-minor signs',n,signs)
Path('workspace/agent4_certificate_notes.txt').write_text('Exact polynomial telescoping plus rational Machin-formula interval certificates checked n=17,18,19,20. This verifies only the finite shape/scale quadratic matrix, not the nonlinear PDE theorem.\n')