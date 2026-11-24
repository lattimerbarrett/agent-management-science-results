# Independent checks of the two arithmetic ingredients used by the
# all-rank detector (no files in experiments are modified).
import sympy as sp
x=sp.symbols('x')
for p in [3,5,7,11,13,17,19]:
 f=sum(sp.binomial(p,j)*x**(j-1) for j in range(1,p+1))
 norm=int(sp.resultant(f,1+x**(p-1),x))
 print('p =',p,'norm(1+pi^(p-1)) mod p^2 =',norm%(p*p))
 assert norm%p==1 and norm%(p*p)!=1
# Check the root factor depths used in the word evaluation for arbitrary c>=3.
for c in range(3,101):
 a_depth=1;b_depth=c-2
 assert 2*a_depth+b_depth >= c
 assert a_depth+2*b_depth >= c
 assert a_depth+b_depth == c-1
print('All depth inequalities checked; the proof of these inequalities is 2+(c-2)=c and 1+2(c-2)>=c.')