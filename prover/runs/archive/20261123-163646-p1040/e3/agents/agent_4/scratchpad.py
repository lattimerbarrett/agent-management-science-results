from itertools import product
from pathlib import Path
G=list(product(range(2),repeat=6));one=(0,)*6
# Coordinates: (12,13,14,23,24,34).
def mul(x,y):
 a,b,c,d,e,f=x;A,B,C,D,E,F=y
 return (a^A,b^B^(a&D),c^C^(a&E)^(b&F),d^D,e^E^(d&F),f^F)
inv={x:next(y for y in G if mul(x,y)==one and mul(y,x)==one) for x in G}
def com(x,y):return mul(mul(mul(x,y),inv[x]),inv[y])
def closure(gens):
 H={one};todo=[one]
 while todo:
  x=todo.pop()
  for y in gens:
   z=mul(x,y)
   if z not in H:H.add(z);todo.append(z)
 return H
A=(1,0,0,0,0,0);B=(0,0,0,0,0,1);C=(0,0,0,1,0,0)
g=[B,A,mul(A,B),C,A,mul(A,C),C,B,mul(B,C)]
def W(i,j,k):return com(com(g[i],g[j]),g[k])
def power(x,k):
 if k<0:x=inv[x];k=-k
 z=one
 for _ in range(k):z=mul(z,x)
 return z
u=one
for t,a in [((0,5,2),3),((0,2,5),-1),((0,1,1),-4),((1,2,3),-2)]:u=mul(u,power(W(*t),a))
assert u==(0,0,1,0,0,0)
H=set(G);orders=[len(H)]
for r in range(3):
 H=closure(set(com(x,y) for x in H for y in G));orders.append(len(H))
assert orders==[64,8,2,1]
assert closure([A,B,C])==set(G)
print('UT4(F2) lower-central orders:',orders,'actual cubic witness:',u)
Path('workspace/agent4_ut4.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/agent4_ut4.py')")[0])
