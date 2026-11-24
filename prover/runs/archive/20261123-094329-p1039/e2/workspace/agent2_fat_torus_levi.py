# Exact tangential-Levi numerator for rho=(|z|²-1)²+||w||²-epsilon².
import sympy as s
t,e=s.symbols("t e",real=True)
N=s.expand((4*t-2)*(e**2-(t-1)**2)+4*t*(t-1)**2)
assert s.expand(N-(2*(t-(1-e**2))**2+2*e**2*(1-e**2)))==0
# For 0<e<1 and t=|z|², this is strictly positive.
print("Tangential Levi completed-square identity checked.")
