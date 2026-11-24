import sympy as s
t=s.symbols('t', real=True)
print('Convex spectral-tail models satisfying the extremal scalar constraints:')
for r in [2,3,4,5]:
 F=(1-t)**r
 print('r =',r,' integral =',s.integrate(F,(t,0,1)),' F(0)=',F.subs(t,0),' F(1)=',F.subs(t,1),' second derivative =',s.factor(s.diff(F,t,2)))
print('Thus full support, norm one, convexity and a strict bound below 1/2 alone do not select 1/3.')
