import sympy as s
eta,u=s.symbols('eta u', real=True)
assert s.expand((u-eta)+(1-u-eta)) == 1-2*eta
print('Upper-bound certificate: (u-eta)+(1-u-eta) =',s.expand((u-eta)+(1-u-eta)))
print('Thus the two nonnegative terms force eta <= 1/2.')
print('Valid implication: witness => failure of positive additivity.')
print('No converse or quasitracial-completeness assertion is used.')
