from fractions import Fraction as F
# Transition2->4; zero-demand cases need no bound.
for l in range(3):
 for r in range(5):
  demand=abs(F(l,2)-F(r,4))
  if not demand:continue
  c0=(6-r if l==2 else 2+r if l==0 else max(3-r,r-1))
  while (c0-l-r)%2:c0+=1
  assert F(c0,6)>=demand,(l,r,c0,demand)
# Equalwidth capacities, after excluded size4refinement in width2.
for sig in [-2,-1,1,2]:
 c=6 if abs(sig)==2 else 3
 assert F(c,6)>=F(abs(sig),2)
for sig in range(1,5):assert F(sig+2,6)>=F(sig,4)
# Nonsingleton budgets and singletoncharges, worsth.
assert F(7,6)-(F(7,12)+F(4,9))==F(5,36)
assert F(6,6)-(F(6,12)+F(7,24))==F(5,24)
assert F(7,6)-(F(7,12)+F(5*8,288))==F(4,9)
assert F(4,9)>=2*F(5,24)
assert F(3,4)>=2*F(5,24)
assert F(9,16)>=2*F(5,24)
# Endpointmargins.
assert F(9,12)-F(2,9)==F(19,36)>F(139,270)
assert F(10,12)-F(5,18)==F(5,9)>F(139,270)
assert F(7,6)-F(1,4)-F(3,14)==F(59,84)>F(139,270)
assert F(8,6)-F(1,4)-F(3,8)==F(17,24)>F(139,270)
assert F(15,12)<=F(15,6)-F(139,135)
print('All independent d6odd transition and energy arithmetic checks passed')
