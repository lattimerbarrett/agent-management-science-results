import sympy as s
import numpy as np
import sys
from pathlib import Path
sys.path.insert(0,'workspace')
from agent4_spectral_experiment import gram

def exact_shape_gram(n,l,J):
    assert l in [1,2,3]
    a=s.Rational(n-2,2)+l;z=s.symbols('z')
    def R(v):
        if v==0:return s.Integer(0) # only l1; kernel contributes zero
        p=s.prod(z-(a-1-t)**2 for t in range(v-1))
        return 2**s.Integer(1-v)*p/(s.factorial(v-1)*s.rf(a+s.Rational(1,2)-v,v-1))
    b=[s.expand(sum((-1)**(j-r)*s.binomial(j,r)*2**r*R(l-1+r) for r in range(j+1))) for j in range(J+1)]
    maxr=2*J+l-2
    U=[s.Integer(1)]
    for r in range(maxr): U.append(s.expand(U[-1]*(z-(a-l-1-2*r)**2)))
    beta=s.Rational(l+1,2)
    moments=[]
    for r in range(maxr+1):
        assert a>l+1+r,(n,l,J,r)
        E=s.gamma(beta)*s.gamma(beta+r)/(s.gamma(a-beta)*s.gamma(a-beta-r))
        O=s.gamma(beta+s.Rational(1,2))*s.gamma(beta+s.Rational(1,2)+r)/(s.gamma(a+s.Rational(1,2)-beta)*s.gamma(a+s.Rational(1,2)-beta-r))
        moments.append(s.simplify(4**r*(E+O)/(a-l-1-r)))
    I1=2**(2*a-1)*s.gamma(a-s.Rational(1,2))*s.gamma(a+s.Rational(1,2))/s.gamma(2*a)
    C={1:2,2:8,3:32}[l]*s.gamma(a)**2/s.pi*I1**2
    G=s.zeros(J+1)
    for i in range(J+1):
        for j in range(i,J+1):
            p=b[i]*b[j]
            if l==1:p*=z-a*a
            if l==3:p=s.cancel(p/(z-(a-1)**2))
            p=s.Poly(s.expand(p),z);value=0
            for r in range(p.degree() if not p.is_zero else -1,-1,-1):
                c=p.nth(r);value+=c*moments[r];p=s.Poly(p.as_expr()-c*U[r],z)
            assert p.as_expr()==0
            G[i,j]=G[j,i]=s.simplify(C*value)
    return G

if __name__=='__main__':
    for l in [1,2,3]:
        E=np.array(exact_shape_gram(25,l,2).evalf(),float)
        if l==1:
            # Existing independent quadrature divides 0/0 at kernel; reimplement with q1+.
            from scipy.special import roots_jacobi,eval_jacobi,gammaln
            n=25;m=n-1;al=(m-2)/2+l
            t,w=roots_jacobi(1000,al,al);r2=(1-t)/(1+t)
            gs=[]
            for j in range(3):
                if j==0:g=np.zeros_like(t)
                else:g=(2*(1-l-2*j)*r2**j+4*j*(2*l+m+2*j-2)/m*r2**(j-1)/(1+t))/(1+t)**l
                gs.append(g)
            gs=np.array(gs);B=np.zeros((3,3))
            for q in range(1,350):
                logh=(2*al+1)*np.log(2)-np.log(2*q+2*al+1)+2*gammaln(q+al+1)-gammaln(q+1)-gammaln(q+2*al+1)
                coeff=(gs*w)@(eval_jacobi(q,al,al,t)*np.exp(-logh/2));k=l+q
                D=2*np.exp(gammaln((k+n+1)/2)+gammaln(k/2)-gammaln((k+n)/2)-gammaln((k-1)/2))
                B+=np.outer(coeff,coeff)/D
        else:B=gram(25,l=l,J=2,Q=350,N=1000)
        print('l',l,'entry ratios exact/independent quadrature',E[1:,1:]/B[1:,1:])
