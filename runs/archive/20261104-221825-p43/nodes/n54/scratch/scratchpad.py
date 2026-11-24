from fractions import Fraction as F
# Units are 4*pi; q lowers action by one unit.
c={'1':F(0),'a':F(-1,2),'b':F(-1,2),'ab':F(-1)}
products={'a':{'1':('a',0),'a':('1',1),'b':('ab',0),'ab':('b',1)},'b':{'1':('b',0),'a':('ab',0),'b':('1',1),'ab':('a',1)}}
for factor,table in products.items():
 for x,(y,k) in table.items():
  lhs=c[y]-k
  print(f'c({factor}*{x})={lhs} < c({x})={c[x]}:',lhs<c[x])
print('Action cosets modulo 4*pi:',sorted({v%1 for v in c.values()}))
print('Thus these strict multiplicative inequalities require only two action cosets, not three.')
