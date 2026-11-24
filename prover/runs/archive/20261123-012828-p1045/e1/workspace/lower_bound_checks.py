"""Exact algebra and finite construction checks for the book Ramsey lower bound.
Run with Python; requires sympy and numpy. No numerical optimization used.
"""
import sympy as s
import numpy as np


def exact_checks():
    p=s.symbols("p", positive=True)
    D=1+2*(1-p)**2
    A=p**2/D
    C=3/D
    # The radical expression is equivalently the positive solution of this equation.
    assert s.factor((3*C+6*A-3)**2-48*A*C)==0
    assert s.simplify(A.subs(p,s.Rational(1,2))-s.Rational(1,6))==0
    assert s.simplify(C.subs(p,s.Rational(1,2))-2)==0
    # Equality with homogeneous model is sqrt(A/C)+sqrt(1/C)=1.
    # On our p interval, this is p/sqrt(3)+sqrt(D/3)=1.
    # Squaring (positive sides) leaves a linear nonzero root in p.
    intersection=s.factor(D-(s.sqrt(3)-p)**2)
    pstar=4-2*s.sqrt(3)
    assert s.simplify(intersection.subs(p,pstar))==0
    astar=(52-16*s.sqrt(3))/121
    assert s.simplify(A.subs(p,pstar)-astar)==0
    assert s.simplify(s.diff(A,p)-2*p*(3-2*p)/D**2)==0
    # Between 1/2 and pstar: 3C+6alpha-3 positive, so radical root is correct.
    assert s.simplify(3*C+6*A-3-12*p/D)==0
    # Blue cross-edge codegree never exceeds within-class codegree.
    q=1-p
    assert s.expand(1+2*q*q-(2*q+q*q))==p*p
    # Remaining intersections, using t=sqrt(alpha).
    t=s.symbols("t", positive=True)
    equation=s.factor((3*(1+t)**2-3-2*t*t)**2-16*t*t*(3-2*t*t))
    assert s.expand(equation-t*t*(33*t*t+12*t-12))==0
    # Unique positive root since polynomial derivative is positive on t>0.
    tstar=(-2+4*s.sqrt(3))/11
    assert s.simplify(tstar*tstar-astar)==0
    print("Exact lower-bound identities and unique transition verified.")


def construction(alpha, n, epsilon, rng):
    astar=float((52-16*s.sqrt(3))/121)
    if alpha<=1/6:
        C=2.
    elif alpha<astar:
        C=1+2*alpha/3+4*np.sqrt(alpha*(3-2*alpha))/3
    else:
        C=(1+np.sqrt(alpha))**2
    N=int(np.floor((C-epsilon)*n))
    if alpha<=1/6:
        classes=np.arange(N)%2
        red=classes[:,None]!=classes[None,:]
    elif alpha<astar:
        classes=np.arange(N)%3
        p=np.sqrt(3*alpha/C)
        raw=rng.random((N,N))<p
        red=np.triu(raw,1)&(classes[:,None]!=classes[None,:])
        red=red|red.T
    else:
        p=np.sqrt(alpha)/(1+np.sqrt(alpha))
        red=np.triu(rng.random((N,N))<p,1)
        red=red|red.T
    np.fill_diagonal(red,False)
    return red


def booksize(adjacency):
    # Matrix-square entry gives the EXACT common-neighbor count.
    a=adjacency.astype(np.int64)
    c=a@a
    return int(np.max(c[adjacency],initial=0))


def finite_checks():
    rng=np.random.default_rng(193021)
    # eps is deliberately generous so modest samples demonstrate the construction.
    for alpha in [.10,1/6,.18,.20072055437105754,.25,.5,1.]:
        n=700
        red=construction(alpha,n,.7,rng)
        blue=~red
        np.fill_diagonal(blue,False)
        br,bb=booksize(red),booksize(blue)
        assert br<np.ceil(alpha*n),(alpha,br)
        assert bb<n,(alpha,bb)
        print(f"alpha={alpha:.9f}, N={len(red)}, red book={br}, blue book={bb}")


if __name__=="__main__":
    exact_checks()
    finite_checks()
