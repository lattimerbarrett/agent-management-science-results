import sympy as s
x,b=s.symbols('x b', real=True)
R=4-(x-1)**2
print('fiber radius squared:',s.factor(R))
print('w Levi entry:',s.diff((x-1)**2,x)+x*s.diff((x-1)**2,x,2))
print('rho at critical w moduli x=0,1 and zprime=0:', [(j,s.expand((x-1)**2-4).subs(x,j)) for j in [0,1]])
print('rho range lower bound = -4; boundary regular because critical points have rho=-3 or -4')
print('For psi=-log(-rho), Hpsi=(-1/rho)Hrho+(1/rho**2)partial(rho)partialbar(rho).')
for n in range(2,7):
 print('n=',n,'positive directions on {v_w=0}:',n-1,'; q=2<n:',2<n)
print('At zprime=(sqrt(3),0,...), w=0: rho=0, w tangent, Levi=-2.')