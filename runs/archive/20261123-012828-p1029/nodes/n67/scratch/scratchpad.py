import sympy as s
eta,u=s.symbols('eta u', real=True)
print('Upper-bound certificate:',s.expand((u-eta)+(1-u-eta)))
print('Hence eta <= 1/2 follows from monotonicity and the two nonnegative terms.')
for x in [s.Rational(1,20),s.Rational(1,4),s.Rational(1,2)]:
    print('Scalar persistent-defect model: eta =',x,', tau(a_n)=1/2, defect =',-x)
print('The scalar constraints alone allow every eta in (0,1/2],')
print('but they are not an operator-algebra construction.')
