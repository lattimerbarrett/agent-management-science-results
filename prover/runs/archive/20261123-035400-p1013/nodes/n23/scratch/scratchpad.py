import math
for r in range(3,13):
 hub=(r/(r-1))**2
 distributed=math.exp(2/(r-1))
 print(r,'a=',1/r,'hub cycle factor=',hub,'two-matchings factor=',distributed,'ratio=',distributed/hub)
# Edges of the hub construction K1 join (balanced T on n-1 with 2 matching edges).
for r in [3,4,5]:
 for s in [10,11,12]:
  n=r*s+1;t_rs=r*(r-1)*s*s//2;t_n=t_rs+(r-1)*s
  hub=t_rs+r*s+2
  print('r,n',r,n,'hub surplus',hub-t_n,'target n/r',n/r)
