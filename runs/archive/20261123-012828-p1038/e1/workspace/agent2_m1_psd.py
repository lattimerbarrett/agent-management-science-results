"""Exact check of the m=1 PSD-coefficient reformulation, not a proof of positivity."""
import sympy as s
from random import Random

def check(trials=40):
    rng=Random(229);T=s.Symbol("T");count=0
    for trial in range(trials):
        k=rng.randint(1,8);c=s.Rational(rng.randint(1,9),rng.randint(1,9))
        xs=sorted([s.Rational(rng.randint(1,30),rng.randint(1,10)) for _ in range(k)])
        tau=s.Rational(rng.randint(1,9),rng.randint(1,9))
        ys=[(x+c*tau)/(1+tau) for x in xs]
        Q=s.zeros(k,k+2)
        for i,(x,y) in enumerate(zip(xs,ys)):
            Q[i,i]=1;Q[i,i+1]=-x-y;Q[i,i+2]=x*y
        N=Q.nullspace();assert len(N)==2
        A=(1-c*T)*s.prod(T+x for x in xs)
        B=(T+c)*s.prod(T+y for y in ys)
        u=s.expand((A+c*B)/(1+c*c));v=s.expand((B-c*A)/(1+c*c))
        F=s.eye(2);last=s.zeros(2)
        for x,y in zip(xs,ys):
            H=s.Matrix([[x+c*c*y,c*(y-x)],[c*(y-x),c*c*x+y]])/(1+c*c)
            Delta=H-last
            assert Delta[0,0]>=0 and Delta[1,1]>=0 and Delta.det()>=0
            last=H;F=F*(T*s.eye(2)+H)
        F=F.applyfunc(s.expand)
        assert (F*s.Matrix([1,T])-s.Matrix([u,v])).applyfunc(s.expand)==s.zeros(2,1)
        ring=s.Matrix([[u.coeff(T,e),v.coeff(T,e)] for e in range(k+2)])
        K=s.Matrix.hstack(*N).T*ring
        rhs=s.zeros(2)
        for e in range(k+1):
            Fe=F.applyfunc(lambda p:p.coeff(T,e))
            assert Fe[0,0]>=0 and Fe[1,1]>=0 and Fe.det()>=0
            Ge=s.Matrix([[N[0][e],N[0][e+1]],[N[1][e],N[1][e+1]]])
            rhs+=Ge*Fe;count+=1
        assert K==rhs
    return {"cases":trials,"PSD_coefficient_matrices":count}

if __name__=="__main__":print(check())
