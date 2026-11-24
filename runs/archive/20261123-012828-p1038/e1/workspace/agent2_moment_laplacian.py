"""Exact rational checks of cyclic moment -> Laplacian -> Q positivity."""
import sympy as s

def check(max_m=15):
    T=s.Symbol("T");z=s.Symbol("z");r=s.Rational(2);R=s.Rational(3)
    nodes=[s.Rational(1,10),s.Rational(1,3),s.Rational(1,2)]
    weights=[s.Rational(2),s.Rational(3),s.Rational(5)]
    total=0
    for m in range(2,max_m+1):
        q=[sum(w*(1+a**m)/(1-a**m) for a,w in zip(nodes,weights))]
        for j in range(1,m):q.append(sum(w*(a**j+a**(m-j))/(1-a**m) for a,w in zip(nodes,weights)))
        c=[R*q[(j+1)%m]-r*q[j] for j in range(m)]
        assert all(c[j]>c[j-1] for j in range(1,m))
        C=s.Matrix(m,m,lambda i,j:c[(i-j)%m])
        S=s.Matrix(m,m,lambda i,j:1 if (i-j)%m==1 else 0)
        D=s.eye(m)-S;L=-D*C
        assert all(L[i,j]<0 for i in range(m) for j in range(m) if i!=j)
        assert L*s.ones(m,1)==s.zeros(m,1)
        minorD=D[:m-1,:m-1];minorL=L[:m-1,:m-1]
        assert minorD.det()==1
        B=minorD.inv()*minorL
        cp=B.charpoly(z).as_expr()
        cof=s.Poly(s.expand((-T)**(m-1)*cp.subs(z,-1/T)),T)
        assert all(c>0 for c in cof.all_coeffs())
        char=C.charpoly(z).as_expr()
        full=s.Poly(s.expand(T**m*char.subs(z,1/T)),T)
        quotient,remainder=s.div(full,s.Poly(1-sum(c)*T,T))
        assert remainder.is_zero
        assert quotient==cof
        total+=len(cof.all_coeffs())
    return {"max_m":max_m,"exact_positive_coefficients":total}

if __name__=="__main__":print(check())
