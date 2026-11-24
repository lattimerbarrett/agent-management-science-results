import sympy as s

def check():
    checked = 0
    for m in range(1, 21):
        # Rational unit vectors from the parametrization of the circle.
        t=s.Rational(m,21)
        u=s.Matrix([(1-t*t)/(1+t*t), 2*t/(1+t*t)])
        v=u*s.Matrix([[1,0]])
        p=u*u.T
        e=s.diag(1,0)
        assert s.simplify(v.T*v-e)==s.zeros(2)
        assert s.simplify(v*v.T-p)==s.zeros(2)
        assert s.simplify(p*p-p)==s.zeros(2)
        assert s.trace(p)==1
        # q(p)=q(e)=1/2 follows from equivalence and 1=e+(1-e).
        for lam in [s.Rational(0),s.Rational(1,7),s.Rational(2,3),s.Rational(1)]:
            for mu in [s.Rational(0),s.Rational(1,5),s.Rational(3,4),s.Rational(1)]:
                a=lam*p+mu*(s.eye(2)-p)
                assert s.simplify(s.trace(a)/2-(lam+mu)/2)==0
                checked += 1
    print(f'Passed {checked} exact rational spectral-decomposition checks and 20 partial-isometry checks.')

if __name__=='__main__':
    check()
