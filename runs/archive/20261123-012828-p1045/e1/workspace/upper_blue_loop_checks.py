"""Exact certificate checks for all-blue-loop weighted matrix lemma."""
import sympy as s
import numpy as np


def exact_checks():
    k,L,c,a,D=s.symbols('k L c a D', positive=True)
    # Root identity c=(2L-L²/(k-1))/k.
    cL=(2*L-L**2/(k-1))/k
    assert s.simplify((L**2-2*L+k*cL)/(k*(k-1))-(k-2)*L**2/(k*(k-1)**2))==0
    # D>=L>=1 makes second bound monotone.
    assert s.diff(D**2-2*D+k*c,D)==2*D-2
    assert s.factor(1-2*(k-1)+k*(k-1)/2)==(k-2)*(k-3)/2
    # Envelope of complete-k balanced constructions is minimized at k=3 or infinity.
    t,z=s.symbols('t z',positive=True)
    f=1-2*z*(1+t)/s.sqrt(1+2*t)+z*z*(1+t)
    assert s.simplify(s.diff(f,t,2)+2*z*(1-t)/(1+2*t)**s.Rational(5,2))==0
    assert s.simplify(f.subs(t,0)-(1-z)**2)==0
    assert s.simplify(f.subs(t,1)-(1+2*z*z-4*z/s.sqrt(3)))==0
    print('Exact all-blue-loop matrix lemma algebra verified.')


def brute_checks():
    rng=np.random.default_rng(20251001)
    count=0
    for m in range(3,13):
        for trial in range(100):
            raw=rng.uniform(0,.9,(m,m))
            P=(raw+raw.T)/2
            P[rng.random((m,m))<.12]=0
            P=np.maximum(P,P.T)
            np.fill_diagonal(P,0)
            w=rng.dirichlet(np.ones(m))
            common=(P*w)@P.T
            A=np.max(common[P>0],initial=0)
            B=np.max(((1-P)**2)@w)
            rhs=min(.5,1+2*A-4*np.sqrt(A/3),(1-np.sqrt(A))**2)
            assert B+1e-12>=rhs,(P,w,A,B,rhs)
            count+=1
    print(f'Checked weighted-matrix inequality on {count} seeded examples.')


if __name__=='__main__':
    exact_checks()
    brute_checks()
