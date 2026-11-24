import sympy as s
eta,t=s.symbols('eta t',real=True)
print('Feasible quasitrace values:',s.reduce_inequalities([t>=eta,t<=1-eta],t))
print('At eta=1/2:',s.reduce_inequalities([t>=s.Rational(1,2),t<=s.Rational(1,2)],t))
print('Threshold bound for h in [0,1], tau(h)=1/2:')
u=s.symbols('u',positive=True)
print('tau(1_(u,1](h)) >=',s.factor((s.Rational(1,2)-u)/(1-u)))