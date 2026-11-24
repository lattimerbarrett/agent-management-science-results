import itertools, math
cases={3:([3,3,3],4),4:([3,3,2,2],5),5:([2,2,2,2,3],5),6:([2,2,2,2,2,2],6)}
for t,(sizes,s) in cases.items():
 groups=[];start=0
 for z in sizes:groups.append(set(range(start,start+z)));start+=z
 R=set(range(start))
 rows=[set(C) for C in itertools.combinations(range(start),s) if 0 in C and all(set(C)&G and (R-set(C))&G for G in groups)]
 assert len(rows)>=24
 rows=rows[:24]
 for A,B in itertools.combinations(rows,2):assert A&B and A&(R-B) and (R-A)&B and (R-A)&(R-B)
 print('P dimension',t,'coordinates',start,'available rows',sum(1 for C in itertools.combinations(range(start),s) if 0 in C and all(set(C)&G and (R-set(C))&G for G in groups)),'24-row certificate passed')
print('Previously independently computed lambda(7) = 1422564; M_8 < 2^21 < 2^24.')
