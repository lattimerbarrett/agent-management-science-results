import sympy as s
eta,c=s.symbols('eta c', positive=True)
print('Under b_n = c*a_n + t*1, the increment is', s.expand(c*eta))
print('For any target 0<delta<=eta, choose c=delta/eta and t=0.')
print('The order isomorphism x -> c*x+t*1 preserves existence and absence of suprema.')