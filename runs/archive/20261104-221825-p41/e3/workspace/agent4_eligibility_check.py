import itertools,json,sys
sys.path.insert(0,'workspace')
from agent3_check import appendable
checked=0
for n in [5,6]:
 allfs=[sum(1<<v for v in q)for q in itertools.combinations(range(n),4)]
 for bits in range(1,1<<len(allfs)):
  fs=tuple(f for i,f in enumerate(allfs)if bits>>i&1)
  V=0
  for f in fs:V|=f
  if V!=(1<<n)-1:continue
  tris={f^(1<<v)for f in fs for v in range(n)if f>>v&1}
  edges={sum(1<<v for v in pair)for f in fs for pair in itertools.combinations([v for v in range(n)if f>>v&1],2)}
  for f in allfs:
   if f in fs:continue
   ct=sum((f^(1<<v))in tris for v in range(n)if f>>v&1)
   ce=sum(sum(1<<v for v in pair)in edges for pair in itertools.combinations([v for v in range(n)if f>>v&1],2))
   predicted=ct>=3 or(ct==2 and ce==5)
   assert predicted==appendable(fs,f),(fs,f,ct,ce)
   checked+=1
print('verified exact tetra eligibility',checked)
open('workspace/agent4_eligibility_check.py','w').write(open(__file__).read())
