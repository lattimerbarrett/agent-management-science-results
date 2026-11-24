from fractions import Fraction as F
for a in range(7,12):assert F(3,2*(12-a))<=F(a,4)-F(15,16),(a,F(3,2*(12-a)))
for a in [12,13]:assert F(7*(a-1),48)<=F(a,4)-F(15,16)
assert F(3*14-1,16)==F(14,4)-F(15,16)
assert F(7*8-8,48)<=F(8,4)-F(15,16)
assert F(7-1,8)<=F(7,4)-F(15,16)
for k in range(100):
 assert k*(k+1)>=6*k-6
 assert k*k+3*k+3>=6*k+1
assert 5*12>=58
print('Degree6 exact finite and boundary inequalities passed')
