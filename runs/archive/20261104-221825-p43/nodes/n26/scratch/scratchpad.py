import sympy as s
r,theta=s.symbols('r theta',real=True)
g=s.cos(theta)
h=(2-r)*g
F=s.exp(1-1/r**2)*g
print('Same boundary values:',s.simplify(h.subs(r,1)-F.subs(r,1)))
print('Old outward derivative at theta=0:',s.diff(h,r).subs({r:1,theta:0}))
print('New outward derivative at theta=0:',s.diff(F,r).subs({r:1,theta:0}))
print('Tangential derivative there:',s.diff(g,theta).subs(theta,0))
print('Thus matching boundary values alone cannot justify the replacement collar.')