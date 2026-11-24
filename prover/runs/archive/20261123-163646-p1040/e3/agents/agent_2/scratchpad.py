from pathlib import Path
# Independent 16-bit representation of UT4(F2).
I=sum(1<<(4*i+i) for i in range(4))
def mm(a,b):
 c=0
 for i in range(4):
  for j in range(4):
   bit=0
   for k in range(4):bit^=((a>>(4*i+k))&1)*((b>>(4*k+j))&1)
   c|=bit<<(4*i+j)
 return c
def mi(a):
 b=a
 while mm(a,b)!=I:b=mm(b,a)
 return b
def cc(a,b):return mm(mm(mm(a,b),mi(a)),mi(b))
def gen(S):
 H={I};todo=[I]
 for h in todo:
  for s in S:
   x=mm(h,s)
   if x not in H:H.add(x);todo.append(x)
 return H
A=I^(1<<1);C=I^(1<<6);B=I^(1<<11)
G=gen([A,B,C]);assert len(G)==64
H=G;orders=[len(H)]
while len(H)>1:
 H=gen([cc(h,g) for h in H for g in G]);orders.append(len(H))
assert orders==[64,8,2,1]
g=[B,A,mm(A,B),C,A,mm(A,C),C,B,mm(B,C)]
def vv(i,j,k):return cc(cc(g[i],g[j]),g[k])
def power(a,k):
 if k<0:a=mi(a);k=-k
 out=I
 for _ in range(k):out=mm(out,a)
 return out
u=I
for c,t in [(3,(0,5,2)),(-1,(0,2,5)),(-4,(0,1,1)),(-2,(1,2,3))]:u=mm(u,power(vv(*t),c))
assert u==I^(1<<3)
print('UT4 group/lower-central orders',orders,'u = I+E14 verified')
source=Path('scratchpad.py').read_text().split("source=Path('scratchpad.py')")[0]
Path('workspace/agent2_ut4_independent.py').write_text(source)
