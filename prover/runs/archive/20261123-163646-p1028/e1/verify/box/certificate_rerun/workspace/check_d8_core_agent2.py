from fractions import Fraction as Q
for q in range(100):
 r=q//2;g=r*(r+1) if q%2==0 else (r+1)**2
 assert Q(g)>=Q(q*q,4)+Q(q,2)
for a in range(1,1000):
 W=6*a-3
 assert Q(W*W,2*a)+W>24*(a-1)
for a in range(11,1000):assert Q(a,12)-Q(1,18)+Q(1,2)<=Q(a,8)
for n in range(17,1000):assert Q(3*n-4,36)<=Q(n,8)-Q(139,180)
assert Q(1,16)+Q(1,2)<1
assert Q(1,2)+Q(1,2)<Q(9,8)
for h in [2,4,6]:assert Q(h*h,32*(8-h))<=Q(10,8)-Q(h,32)-Q(1,4)
print('All d8 core DAG, budget, residual dense-case, full-connectivity exact checks passed.')
