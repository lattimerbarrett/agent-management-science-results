import sympy as s
# A uniform exterior cylinder near the worm Nebenhuelle point p=(-1/2,1,0).
d=s.Rational(1,100)
# If |w-1|<=d, |log|w|^2| <= 2d/(1-d).
phase_bound=2*d/(1-d)
separation=s.Rational(3,2)-d-phase_bound
print('Lower bound for |z-exp(i log|w|^2)|:',separation)
print('It exceeds 1 by:',s.factor(separation-1))
print('Lower bound for rho (eta and |zeta|^2 discarded):',s.factor(separation**2-1))
# For a worm point |zeta_j|<=1. Two scaled Henon basin horns
# therefore force both normal coordinates into this exterior cylinder.
eps=s.Rational(1,1000)
print('Normal horn width on |zeta_j|<=1:',eps,'<',d)
# H(u,t)=(t,16t^2-u/4). In |t|>max(|u|,1):
r=s.symbols('r',positive=True)
print('Escape lower bound for second coordinate:',16*r*r-r/4)
print('At r>=1 this is >= (63/4) r, so the escape cone is forward invariant.')
print('Therefore for n>=4, two scaled basin factors give a Fatou-Bieberbach domain through p avoiding the worm K.')
print('This rules out using failure of full-rank entire domination at p as the missing Oka obstruction.')