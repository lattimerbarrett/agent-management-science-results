"""Exact polynomial Bezoutian degree/rank checks for the Pick obstruction."""
import sympy as S

def check(maxdegree=12):
    z,t=S.symbols('z t')
    done=0
    for d in range(maxdegree+1):
        # symbolic real and imaginary parts, not a floating-point sample
        aa=S.symbols('a:'+str(d+1),real=True)
        bb=S.symbols('b:'+str(d+1),real=True)
        pp=[a+S.I*b for a,b in zip(aa,bb)]
        p=lambda zz:sum(c*zz**j for j,c in enumerate(pp))
        ps=lambda zz:sum(S.conjugate(c)*(-zz)**j for j,c in enumerate(pp))
        # t represents conjugate(w)
        numerator=S.expand(ps(z)*sum(c*(-t)**j for j,c in enumerate(pp))-p(z)*sum(S.conjugate(c)*t**j for j,c in enumerate(pp)))
        quotient,remainder=S.div(numerator,z+t,z)
        assert S.expand(remainder)==0
        if d==0:assert S.expand(quotient)==0
        else:
            P=S.Poly(S.expand(quotient),z,t)
            assert P.degree(z)<=d-1 and P.degree(t)<=d-1
            # Explicit separable rank<=d factorization.
            matrix=S.Matrix(d,d,lambda i,j:P.coeff_monomial(z**i*t**j))
            recovered=sum(matrix[i,j]*z**i*t**j for i in range(d) for j in range(d))
            assert S.expand(recovered-quotient)==0
        done+=1
    return done

if __name__=='__main__':print('exact degrees checked:',check())
