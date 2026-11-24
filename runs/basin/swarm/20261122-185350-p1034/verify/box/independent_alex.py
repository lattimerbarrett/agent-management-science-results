from sage.all import *
p=[-3,-3,3,5,7]
V=matrix(QQ,4,4)
for i in range(4):
    V[i,i]=QQ(p[i]+p[i+1])/2
for i in range(3):
    V[i,i+1]=-QQ(p[i+1]-1)/2
    V[i+1,i]=-QQ(p[i+1]+1)/2
T=LaurentPolynomialRing(QQ,'t');t=T.gen()
print(V)
x=(t*V-V.transpose()).det()/t**2
print(x, x(t=1))
