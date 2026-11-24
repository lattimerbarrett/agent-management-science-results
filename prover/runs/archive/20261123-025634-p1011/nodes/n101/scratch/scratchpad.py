import sympy as s
r,n,A,B=s.symbols('r n A B', positive=True)
G=A*r**(2-n)+B
integrand=(n-2)*G*s.diff(G,r)/2-r*s.diff(G,r)**2/2+r*s.diff(G,r)**2
P=s.simplify(r**(n-1)*integrand)
print('Pohozaev flux divided by hemisphere area =',s.expand(P))
print('radial derivative =',s.simplify(s.diff(P,r)))
