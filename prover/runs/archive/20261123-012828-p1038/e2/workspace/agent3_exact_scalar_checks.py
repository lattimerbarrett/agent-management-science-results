from fractions import Fraction as F
bounds=[(F(30),F(1),F(83,5000),F(167,10000)),(F(301,10),F(100),F(743,1000),F(93,125)),(F(3,5),F(1),F(283,500),F(567,1000)),(F(1,2),F(100),F(199,200),F(249,250)),(F(1,10),F(99),F(499,500),F(999,1000))]
for d,r,l,h in bounds:
 p=lambda t:r*t*t+2*d*t-r
 assert p(l)<0<p(h)
xl,xh=bounds[0][2:];yl,yh=bounds[1][2:];ul,uh=bounds[2][2:];vl,vh=bounds[3][2:];ql,qh=bounds[4][2:]
assert xh < ul**3 # tau_A<u
assert uh**2 < yl/vh # u<tau_B
assert yh < vl**3 # tau_B<v
assert qh*vh<1
pos=(uh**2+1+xh*uh+xh/ul)*(vh**2+1+yh*vh+yh/vl)
assert pos<F(19,4)
ga_lower=ul*vl+1+xl*ul+xl/vh
assert ga_lower>F(158,100)
assert yl*vl>F(85,100)**2
assert F(158,100)*F(185,100)**2>F(54,10)
print('All exact rational scalar inequalities certified.')
print('positive base upper bound:',pos, float(pos))
