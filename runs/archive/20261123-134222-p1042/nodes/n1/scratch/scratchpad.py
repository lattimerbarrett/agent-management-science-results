import itertools as it, collections
for m in [7]:
 cs=collections.Counter()
 for a in it.product(range(5),repeat=m):
  if any(a.count(i)>2 for i in range(1,5)):continue
  cs[sum(x!=0 for x in a)]+=1
 print(cs,sum(cs.values()))
