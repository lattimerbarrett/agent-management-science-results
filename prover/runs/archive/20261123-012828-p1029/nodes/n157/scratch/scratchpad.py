import sympy as s
I=s.eye(2)
examples=[s.Matrix([[s.Rational(1,3),s.Rational(1,5)],[0,s.Rational(1,4)]]),s.Matrix([[s.Rational(1,2),0],[0,s.Rational(2,3)]])]
for x in examples:
    h=(I+x.T*x).inv()
    g=h.row_join(h*x.T).col_join((x*h).row_join(x*h*x.T))
    J=s.diag(1,1,-1,-1)
    assert g*g==g and g.T==g
    assert g[2:4,0:2]*g[0:2,0:2].inv()==x
    assert (I-x.T*x).is_positive_semidefinite
    assert (g*J*g).is_positive_semidefinite
    print('Exact graph projection and reconstruction checks passed; graph rank =',g.rank())
