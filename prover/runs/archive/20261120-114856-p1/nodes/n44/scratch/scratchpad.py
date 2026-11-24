import sympy as S
z,H,E0,E1=S.symbols('z H E0 E1', positive=True)
l1,l2,l3=S.symbols('l1 l2 l3', real=True)
L=[l1,l2,l3,1-l1-l2-l3]
d=S.symbols('d1:5', real=True)
dx=sum(a*b for a,b in zip(L,d))
expr=2*S.log(1-z*dx/H)+sum(2*a*S.log(1+z*b/H) for a,b in zip(L,d))-2*S.log(1-z*E0/H)-2*S.log(1-z*E1/H)
first=S.simplify(S.diff(expr,z).subs(z,0))
second=S.factor(S.diff(expr,z,2).subs(z,0)/2)
expected=(E0**2+E1**2-dx**2-sum(a*b*b for a,b in zip(L,d)))/H**2
assert S.simplify(first-2*(E0+E1)/H)==0
assert S.simplify(second-expected)==0
print('First-order term:',first)
print('Second-order term verified: (E0^2+E1^2-delta_xi^2-sum L_i delta_i^2)/H^2')
print('No residual weights or inverse residual weights occur.')
print('For |delta_i|,|delta_xi|<=D0 E0 and 0<=E1<=E0:')
print('|quadratic term| <= [2+D0^2(1+sum|L_i|)] E0^2/H^2.')
print('Log cubic remainders are uniformly O(E0^3) once all arguments are within 1/2 of 1.')
