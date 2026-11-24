"""Exact positive local spinor identity for the physical Joukowski curve."""
import sympy as s

def symbolic_test():
    x,y,c,r,R=s.symbols('x y c r R',nonzero=True)
    P=lambda t:s.Matrix([[t*t,t],[t,1]])
    delta=r/x+(R-r)/c-R/y
    F=r*(x-1/x)-R*(y-1/y)+(R-r)*(c-1/c)
    M=r/x*P(x)+(R-r)/c*P(c)-R/y*P(y)
    assert all(s.factor(v)==0 for v in M-delta*s.eye(2)-s.diag(F,0))
    # On F=0 this is delta*(1+y^2)=sum of positive squares.
    err=s.factor(delta*(1+y*y)-r/x*(x-y)**2-(R-r)/c*(c-y)**2)
    assert s.factor(err+F)==0
    T=s.symbols('T')
    Q=lambda t:(T+t)*(1-t*T)
    assert s.factor(R/y*Q(y)-r/x*Q(x)-(R-r)/c*Q(c)-F*T)==0
    return True

def rational_tests():
    from fractions import Fraction as F
    P=lambda t:((t*t,t),(t,F(1)))
    count=0
    for c in [F(1,5),F(1,2),F(4,5)]:
        H=lambda t:(t-c)*(1+c*t)/t
        for x in [F(1,20),F(1,10),F(1,3),F(2,3),F(1),F(2),F(5)]:
            if x==c:continue
            for weight in [F(1,10),F(1,3),F(1,2),F(4,5)]:
                y=weight*x+(1-weight)*c
                r=F(1);R=H(x)/H(y)
                assert R>r
                delta=r/x+(R-r)/c-R/y
                assert delta>0
                assert delta*(1+y*y)==r/x*(x-y)**2+(R-r)/c*(c-y)**2
                for i in range(2):
                    for j in range(2):
                        assert r/x*P(x)[i][j]+(R-r)/c*P(c)[i][j]-R/y*P(y)[i][j]==(delta if i==j else 0)
                count+=1
    return count

if __name__=='__main__':
    print('Symbolic identities:',symbolic_test())
    print('Exact rational positive examples:',rational_tests())
