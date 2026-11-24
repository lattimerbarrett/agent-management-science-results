import sympy as s
eta,t,d=s.symbols('eta t d', real=True)
# If 0<=b<=1 and p=1_(t,1](b), abelian functional calculus gives
# b <= t*(1-p)+p, so eta <= t+(1-t)*D(p).
lower=s.solve(s.Eq(eta,t+(1-t)*d),d)[0]
print('Cutoff lower bound D(p) >=', lower)
print('At t=eta/2:',s.factor(lower.subs(t,eta/2)))
print('Because b >= t*p, sum b_n <= 1 gives sum p_n <= (1/t)*1.')
print('At t=eta/2 this is sum p_n <= (2/eta)*1.')
print('Finite-factor projection exhaustion: D(p_n) -> 0.')
print('This contradicts the positive constant lower bound eta/(2-eta).')
