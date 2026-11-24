"""General harmonic blocks, reduced to universal gamma-weight telescope.
Only finite polynomial form positivity is checked, NOT PDE compactness.
"""
import sympy as s
m,k=s.symbols('m k')
def harmonic_matrix(n,ell,d):
    beta=s.Rational(n+1,2);alpha=s.Rational(n+2,2)
    if ell>=2:
        D=s.rf(m-ell+3,ell-2)*s.rf(m+n+2,ell-2)
        jstart=0
        Rs=[s.expand(sum((-1)**(j-a)*s.binomial(j,a)*s.rf(m+1,a)*s.rf(m+n+2-a,a)/(s.rf(ell-1,a)*s.prod(beta-h for h in range(1,a+1))) for a in range(j+1))) for j in range(d+1)]
    elif ell==1:
        D=(m+1)*(m+n+1)
        jstart=1
        Rs=[s.expand(sum((-1)**(j-1-a)*s.binomial(j,a+1)*s.rf(m+2,a)*s.rf(m+n+1-a,a)/(s.factorial(a)*s.prod(s.Rational(n-1,2)-h for h in range(1,a+1))) for a in range(j))) for j in range(1,d+2)]
    elif ell==0:
        D=(m+1)*(m+2)*(m+n)*(m+n+1)
        jstart=2
        Rs=[s.expand(sum((-1)**(j-2-a)*s.binomial(j,a+2)*s.rf(m+3,a)*s.rf(m+n-a,a)/(s.factorial(a)*s.prod(s.Rational(n-3,2)-h for h in range(1,a+1))) for a in range(j-1))) for j in range(2,d+3)]
    else:
        raise ValueError('ell must be nonnegative')
    def telescope(P,p):
        b=s.Rational(p+3,2);c=s.Rational(p+n+1,2)
        rem=s.expand((2*k+p+alpha)*P.subs(m,2*k+p));A=0
        for v in range(s.degree(P,m),-1,-1):
            L=s.expand((k+c-1)**2*k**v-(k+b)**2*(k+1)**v)
            av=s.expand(rem).coeff(k,v+1)/L.coeff(k,v+1)
            A+=av*k**v;rem=s.expand(rem-av*L)
        assert rem==0
        return 16*s.gamma(b)**2/s.gamma(c-1)**2*s.expand(A).coeff(k,0)
    Q=s.zeros(d+1)
    for i in range(d+1):
        for j in range(i,d+1):
            P=s.expand(D*Rs[i]*Rs[j])
            Q[i,j]=Q[j,i]=s.simplify(telescope(P,0)+telescope(P,1))
    return Q

def atan_interval(q,N=60):
    v=sum((-1)**j*s.Rational(1,q)**(2*j+1)/s.Integer(2*j+1) for j in range(N))
    w=v+(-1)**N*s.Rational(1,q)**(2*N+1)/s.Integer(2*N+1)
    return min(v,w),max(v,w)
a,b=atan_interval(5);c,d=atan_interval(239)
pl,pu=16*a-4*d,16*b-4*c
assert pl>3 and pu<4

def polynomial_interval(expr):
    lo=hi=s.Rational(0)
    for (power,),coeff in s.Poly(s.expand(expr),s.pi).terms():
        if coeff>=0:lo+=coeff*pl**power;hi+=coeff*pu**power
        else:lo+=coeff*pu**power;hi+=coeff*pl**power
    return lo,hi

def certify_positive(expr):
    num,den=s.fraction(s.factor(expr))
    dl,du=polynomial_interval(den)
    lo,hi=polynomial_interval(num)
    assert (dl>0 and lo>0) or (du<0 and hi<0)

if __name__=='__main__':
    count=0
    for n in range(5,19):
        dmax=(n-1)//2
        for ell in range(0,dmax+1):
            jstart=2 if ell==0 else 1 if ell==1 else 0
            d=(dmax-ell)//2-jstart
            if d<0:continue
            Q=harmonic_matrix(n,ell,d)
            M=s.Matrix(d+1,d+1,lambda i,j:(ell-1+2*jstart+i+j)*Q[i,j])
            for r in range(1,d+2):
                certify_positive(M[:r,:r].det());count+=1
            print('CERTIFIED PD',n,ell,d,flush=True)
    print('Exact positive leading minors certified:',count)
