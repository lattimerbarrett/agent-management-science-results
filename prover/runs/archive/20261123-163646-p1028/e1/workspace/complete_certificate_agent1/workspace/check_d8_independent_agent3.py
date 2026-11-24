from fractions import Fraction as F
# Genericordinarybudgets afterworstsingletoncharges.
for a in range(8,100):
 E=F(a,12)-F(1,18)
 for h in [2,4]:
  if a<9:continue
  if ('22',a,h) not in [('22',9,4),('22',10,4)]:assert E+F(h,8)<=F(a,8)
 if a>=9 and a not in [9,10]:assert E+F(3,8)+F(1,8)<=F(a,8)
 for h in [2,4,6,8]:
  if a==8 and h!=8:continue
  if (a,h) not in [(8,8),(9,8),(10,8),(9,6)]:assert E+F(h,32)+F(1,4)<=F(a,8)
# Endpointmargins.
gamma=F(139,360)
for a in range(9,14):assert F(2,16-a)<=F(a,8)-F(1,4)-gamma
for a in range(9,13):assert F(13,8*(14-a))<=F(a,8)-F(1,4)-gamma
assert F(71,72)<F(89,90)==F(13,8)-F(1,4)-gamma
assert F(11,12)<F(89,90)
assert F(14,24)-F(7,36)>=gamma
# Directed-flowcapacity W72 impossible atendpointa13.
assert F(36)+F((72-12)**2+72**2,48)+72>2*12*12
print('Independent d8 generic coverage and endpoint arithmetic all passed')
