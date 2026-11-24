import z3,itertools
k=4;n=15;c=7
patterns=[]
for p in itertools.product([0,1,2],repeat=k): # 2=free
 nonfree=[x for x in p if x!=2]
 if nonfree and nonfree[0]==1:continue
 patterns.append(p)
s=z3.Solver();s.set(timeout=110000)
a=[z3.Int('a%d'%j) for j in range(len(patterns))]
s.add(*[z3.And(x>=0,x<=n) for x in a],sum(a)==n)
for i in range(k):s.add(sum(x for x,p in zip(a,patterns) if p[i]==2)==c)
def inter(mask):
 coords=[j for j in range(k) if mask>>j&1]
 dim=sum(x for x,p in zip(a,patterns) if all(p[j]==2 for j in coords))
 conflict=sum(x for x,p in zip(a,patterns) if 0 in [p[j] for j in coords] and 1 in [p[j] for j in coords])
 return z3.If(conflict>0,0,sum(z3.If(dim==i,1<<i,0) for i in range(c+1)))
w=sum((-2)**(mask.bit_count()-1)*inter(mask) for mask in range(1,16))
s.add(w==310,inter(3)==4,inter(12)==1)
res=s.check();print(res,flush=True)
if res==z3.sat:
 print([(p,s.model()[x]) for x,p in zip(a,patterns) if s.model()[x].as_long()])
