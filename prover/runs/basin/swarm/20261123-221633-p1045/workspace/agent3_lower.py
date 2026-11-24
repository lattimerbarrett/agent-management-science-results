"""Exact algebra and concentration certificates for book Ramsey lower bounds."""
import math
import sympy as sp

def coefficients(alpha):
    if not 0 < alpha <= 1:
        raise ValueError("alpha must lie in (0,1]")
    return (2., (math.sqrt(3-2*alpha)+2*math.sqrt(alpha))**2/3,
            (1+math.sqrt(alpha))**2)

def check_algebra():
    p=sp.symbols('p', positive=True)
    den=1+2*(1-p)**2
    a=p*p/den
    c=3/den
    assert sp.simplify(c*a**0 - (1+sp.Rational(2,3)*a+sp.Rational(4,3)*p*(3-2*p)/den))==0
    assert sp.simplify(a-sp.Rational(1,6) - (2*p-1)*(2*p+3)/(6*(2*p**2-4*p+3)))==0
    x=sp.symbols('x',nonnegative=True)
    # c3 >= (1+x)^2 iff sqrt(3-2*x*x) >= sqrt(3)+(sqrt(3)-2)*x.
    rhs=sp.sqrt(3)+(sp.sqrt(3)-2)*x
    diff=sp.expand(3-2*x*x-rhs*rhs)
    assert sp.simplify(diff-x*((4*sp.sqrt(3)-9)*x+4*sp.sqrt(3)-6))==0
    root=sp.simplify((4*sp.sqrt(3)-6)/(9-4*sp.sqrt(3)))
    assert sp.simplify(root-(4*sp.sqrt(3)-2)/11)==0
    astar=sp.expand(root**2)
    assert astar==(52-16*sp.sqrt(3))/121
    assert sp.Rational(1,6)<astar<sp.Rational(21,100)
    return astar

def hoeffding_certificate(alpha,n,eps,kind='tripartite'):
    """Returns (N, union failure upper bound) from exact means.

    A value <1 is a rigorous certificate up to standard floating arithmetic;
    round outward or replace floats by intervals when a formal numeric
    certificate is wanted. Hoeffding itself proves eventual success.
    """
    c2,c3,cr=coefficients(alpha)
    c=c3 if kind=='tripartite' else cr
    N=math.floor((c-eps)*n)
    m=math.ceil(alpha*n)
    if kind=='tripartite':
        p=3*math.sqrt(alpha)/(math.sqrt(3-2*alpha)+2*math.sqrt(alpha))
        sizes=[N//3+(i<N%3) for i in range(3)]
        means_red=[sizes[k]*p*p for k in range(3)]
        means_blue=[sizes[i]-2+(N-sizes[i])*(1-p)**2 for i in range(3)]
        means_blue += [(sizes[i]+sizes[j]-2)*(1-p)+sizes[3-i-j]*(1-p)**2
                       for i in range(3) for j in range(i+1,3)]
    else:
        p=math.sqrt(alpha)/(1+math.sqrt(alpha))
        means_red=[(N-2)*p*p]
        means_blue=[(N-2)*(1-p)**2]
    gap=min([m-mu for mu in means_red]+[n-mu for mu in means_blue])
    failure=1. if gap<=0 else min(1.,N*(N-1)*math.exp(-2*gap*gap/max(1,N-2)))
    return N,failure

if __name__=='__main__':
    print('transition =',check_algebra())
    for a in [0.1,1/6,.18,.2,.21,.5,1]:
        kind='tripartite' if coefficients(a)[1]>coefficients(a)[2] else 'random'
        print(a,coefficients(a),hoeffding_certificate(a,10**8,.01,kind))
