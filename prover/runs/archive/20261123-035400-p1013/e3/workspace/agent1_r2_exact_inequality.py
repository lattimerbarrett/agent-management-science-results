import sympy as s

def exact_certificate():
    k,x=s.symbols('k x',integer=True,nonnegative=True)
    b=3*k; S=0
    for ell in range(6):
        coeff=0
        for c in range(ell//3+1):
            for d in range(ell//2+1):
                a=ell-3*c-2*d
                if a<0:continue
                m=a+d+c
                coeff+=s.prod(k-i for i in range(m))*7**a*9**d/(s.factorial(a)*s.factorial(d)*s.factorial(c))
        ratio=s.Rational(ell,1)/b*(1+(b-ell)*(ell-1))
        weight=1/(s.factorial(ell)*s.prod(b-i for i in range(1,ell+1)))
        S+=(ratio-1)*coeff*weight
    num=786479*k**3-7576531*k**2+14004774*k-7113096
    den=64800*(3*k-4)*(3*k-2)*(3*k-1)
    assert s.factor(S-num/den)==0
    shifted=s.Poly(s.expand(num.subs(k,x+8)),x)
    assert all(c>0 for c in shifted.all_coeffs())
    return s.factor(S),shifted.as_expr()

if __name__=='__main__':print(exact_certificate())
