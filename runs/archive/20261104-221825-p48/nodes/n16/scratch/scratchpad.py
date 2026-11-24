import sympy as s
e=s.symbols('e', nonnegative=True)
def chi(a,b): return s.expand((a+1)*(b+1)-e*a*(a+1)/2)
# Griffiths vanishing: Sym^m E tensor det E tensor K_X is acyclic in higher degrees if E ample.
for m in range(12):
 ans=0
 for i in range(m+1):
  a=5*i-(m-i)+2
  b=-i+(m-i)*(12*e+5)+(11*e+2)
  ans+=chi(a,b)
 print(m,s.factor(ans))
