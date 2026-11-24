import math
from functools import reduce
for c in [5,10,20,50,100,200]:
 vals=[]
 for r in range(3,c+1):
  t=c+r
  sizes=[t//r+(i<t%r) for i in range(r)]
  odd=t%2
  pol=[1]
  for s in sizes:
   if odd and pol==[1]:
    q=[0]+[math.comb(s-1,j-1) for j in range(1,s)]+[0]
   else:
    q=[0]+[math.comb(s,j) for j in range(1,s)]+[0]
   z=[0]*(len(pol)+s)
   for i,a in enumerate(pol):
    for j,b in enumerate(q):z[i+j]+=a*b
   pol=z
  w=pol[t//2]//(1 if odd else 2)
  target=math.comb(c+2,(c+2)//2)/2
  vals.append((math.log2(w/target),r))
 print(c,min(vals))
from pathlib import Path
Path('workspace/agent4_cross_capacity.py').write_text(Path('scratchpad.py').read_text())
