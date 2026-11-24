import sympy as s
qx,qy,qd=s.symbols('qx qy qd', real=True)
defect=qy-qx-qd
print('Additivity defect D(x,d) =', defect)
print('When q(y)=q(x), D(x,d) =', defect.subs(qy,qx))
print('Faithfulness implies q(d)>0 for nonzero positive d, not D(x,d)=0.')
print('The invalid step was replacing q(y)-q(x) by q(y-x) for a noncommuting pair.')
eta=s.symbols('eta', real=True)
print('The valid two-increment constraint remains:', s.solve_univariate_inequality(eta <= 1-eta, eta))