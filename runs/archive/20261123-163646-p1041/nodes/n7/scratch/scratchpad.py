import itertools,collections,random,pickle
for edges in [[(0,1),(2,3),(0,2)],[(0,1),(2,3),(4,5)],[(0,1),(1,2),(2,3)],[(0,1),(0,2),(0,3)]]:
 nc=max(max(x) for x in edges)+1;n=11-nc
 counts=collections.Counter(sum(((x>>a&1)&(x>>b&1))<<i for i,(a,b) in enumerate(edges)) for x in range(1<<nc))
 ls=[]
 for mask in range(1,1<<n):ls.append(sum(1<<x for x in range(1<<n) if (mask&x).bit_count()%2))
 print(edges,n,counts,flush=True)
 for it in range(3000000):
  qs=[]
  for j in range(3):
   v=0
   for _ in range(random.choice([1,2,2,3])):
    a,b=random.sample(ls,2);v^=a&b
   if random.random()<0.3:v^=(1<<(1<<n))-1
   if random.random()<0.2:v^=random.choice(ls)
   qs.append(v)
  a,b,c=qs;vals=[0,a,b,a^b,c,a^c,b^c,a^b^c]
  w=sum(count*vals[mask].bit_count() for mask,count in counts.items())
  if 256<w<320 and w not in {272,288,296,304,308,312,314,316,318}:
   print('NEW',w,edges,qs,flush=True);pickle.dump((edges,qs,n),open('new.pkl','wb'));quit()
