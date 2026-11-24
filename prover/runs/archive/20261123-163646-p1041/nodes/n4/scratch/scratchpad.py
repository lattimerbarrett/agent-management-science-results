import random,itertools,time
n=9
lin=[]
for i in range(n):lin.append(sum(1<<x for x in range(1<<n) if x>>i&1))
qb=[(1<<(1<<n))-1]+lin+[a&b for a,b in itertools.combinations(lin,2)]
g=lin[0]&((lin[1]&lin[2])^(lin[3]&lin[4]))
# random walk among all quadratics
q=0;vals=set();best=1024;t=time.time()
for i in range(100000000):
 q^=random.choice(qb)
 w=g.bit_count()+(g^q).bit_count()
 if w<320:vals.add(w)
print(sorted(vals),time.time()-t)
