import sympy as s
A=s.diag(s.Rational(3,4),s.Rational(1,4))
D=s.Matrix([[s.Rational(1,10),s.Rational(1,20)],[s.Rational(1,20),s.Rational(1,10)]])
E=s.diag(s.Rational(1,100),s.Rational(1,50))
def a(n):return A-D/s.Integer(2)**n-E/s.Integer(4)**n
def positive(B):return B[0,0]>0 and B.det()>0
for n in range(30):
 x,y=a(n),a(n+1)
 assert positive(x) and positive(A-x) and positive(y-x)
 assert (x-s.eye(2)/2).det()<0
 assert (y-s.eye(2)/2).det()<0
 assert x*y-y*x != s.zeros(2)
 # If two rank-one spectral lines agreed, selfadjoint 2x2 matrices commute.
 # Thus the spectral projections above 1/2 have join I for every adjacent pair.
print('30 exact ordered adjacent pairs: positive contractions, one eigenvalue either side of 1/2, noncommuting; high spectral projection joins are I.')
