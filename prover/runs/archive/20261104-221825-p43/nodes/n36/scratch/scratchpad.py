import sympy as s
# Audit both constants in the period estimates.
eps,L,T,D=s.symbols('epsilon L T D',positive=True)
# For a T-periodic orbit, integral_0^T Y(x(t)) dt=0.
# Hence |Y(x(t))| <= L D, and a shortest time arc between
# diametral points has duration at most T/2.
print('Diameter inequality after dividing by D:',s.simplify(eps*L*T*D/(2*D)))
print('Necessary period threshold:',s.solve(s.Eq(1,eps*L*T/2),T)[0])
# Wirtinger instead yields 1 <= (eps L T / (2 pi))^2.
print('Wirtinger necessary threshold:',2*s.pi/(eps*L))
print('For T=1 and epsilon=1/L, the diameter inequality would require 1 <=',s.simplify((eps*L*T/2).subs({eps:1/L,T:1})))
