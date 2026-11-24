from fractions import Fraction as F
import itertools,math

def variance(r,m):
 p=F(1,r);lam=-F(1,r-1)
 return p*(1-p)*(m+2*sum((m-d)*lam**d for d in range(1,m)))
for r in range(3,9):
 for m in range(1,101):
  assert 0<=variance(r,m)<=m*F(1,r)*(1-F(1,r))*(1+F(2,r-2))
for r,m in [(3,m)for m in range(2,9)]+[(4,m)for m in range(2,7)]:
 W=[(i,)for i in range(r)]
 for _ in range(m-1):W=[w+(j,)for w in W for j in range(r)if j!=w[-1]]
 var=sum((F(w.count(0))-F(m,r))**2 for w in W)/len(W)
 assert var==variance(r,m)
 prob=F(sum(w[-1]!=w[0]for w in W),len(W))
 assert prob==F(r-1,r)*(1-(-F(1,r-1))**(m-1))
print('Markov covariance/variance/closure exact checks PASS')
