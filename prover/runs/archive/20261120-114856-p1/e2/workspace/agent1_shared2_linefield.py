import sympy as S
x=S.symbols('x')
B=S.Rational(1,100); t=S.Rational(1,10)
chi=(x*x-1)**2*(x*x-B)-B
p=(x*x-1)*(x-t); q=(x*x-1)*(x+t)

def expectation(num,f):
    return S.Poly(S.rem(S.expand(num*f),chi,x),x).coeff_monomial(x**5)

def derivative_T(num):
    L=lambda f:expectation(num,f)
    H=S.Matrix([[L(x**(i+j)) for j in range(3)] for i in range(3)])
    cf=H.inv()*S.Matrix([-L(x**(3+i)) for i in range(3)])
    poly=x**3+sum(cf[j]*x**j for j in range(3))
    h=L(poly**2)
    out=S.rem(S.expand(num*poly**2/h),chi,x)
    # out must be numerator for measure: expectation with num multiplies d_i.
    # Its degree5 is normalized 1.
    cols=[]
    for k in range(1,6):
        def dL(f):
            rem=S.Poly(S.rem(S.expand(f),chi,x),x)
            return rem.coeff_monomial(x**k)
        dpvec=-H.inv()*S.Matrix([dL(poly*x**j) for j in range(3)])
        dp=sum(dpvec[j]*x**j for j in range(3));dh=dL(poly**2)
        cols.append(S.Matrix([S.cancel((dL(x**j*poly**2)+2*L(x**j*poly*dp)-expectation(out,x**j)*dh)/h) for j in range(1,6)]))
    return out, S.Matrix.hstack(*cols), poly,h

def check():
    for uu,vv in [(S.Rational(0),S.Rational(-1,4)),(S.Rational(1,10),S.Rational(-1,4))]:
        r=x*x+uu*x+vv;num=S.expand(q*r)
        num1,J,p1,h=derivative_T(num)
        num2,J1,q1,h1=derivative_T(num1)
        assert S.expand(p1-p)==0 and S.expand(q1-q)==0
        assert S.rem(num2-num,chi,x)==0 and h==B and h1==B
        N=J1*J-S.eye(5)
        assert N.rank()==1 and N*N==S.zeros(5)
        cr=S.Poly(S.rem(chi,r,x),x);A=cr.coeff_monomial(x);C=cr.coeff_monomial(1);D=C*C-A*C*uu+A*A*vv
        jj=(1+vv)*D+B*((1+vv)*C-uu*A*vv)
        hh=-uu*D+B*(-(1+vv)*A+uu*(A*uu-C))
        for col in N.columnspace():
            du=col[0];dv=col[1]-t*du
            assert S.cancel(jj*du+hh*dv)==0
    print('Exact critical shared2 stationary-pair, nilpotent rank1, and linefield formula checks passed.')
if __name__=='__main__': check()
