from fractions import Fraction as F
n=16;pending=[0,0,0];edges=[]
for v,q in [(1,1)]+[(i,2)for i in range(2,14)]+[(14,1)]:
 if q==1:chosen=[next(x for x in pending if pending.count(x)>1)]
 else:chosen=list(dict.fromkeys(pending));assert len(chosen)==2
 for u in chosen:pending.remove(u);edges.append((u,v))
 pending += [v]*q
edges += [(u,15)for u in pending];assert len(set(edges))==len(edges)==29
curr={e:F(1,3)for e in edges}
for a,b,c in [(0,1,2),(2,3,4)]:
 for e in [(a,b),(b,c)]:curr[e]-=F(1,9)
 curr[(a,c)]+=F(1,9)
assert sum(i*i for i in curr.values())==F(85,27)<F(63,20)
for v in range(n):assert sum(i for(a,b),i in curr.items()if a==v)-sum(i for(a,b),i in curr.items()if b==v)==(1 if v==0 else -1 if v==15 else 0)
print('Auxiliary d5 double-triangle exact flow passed.')
