lines=[(0,1,2),(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
f=[sum(all(x>>j&1 for j in L) for L in lines)%2 for x in range(128)]
print(sum(f))
from collections import Counter
print(Counter(sum(f[x]^((x&a).bit_count()%2) for x in range(128)) for a in range(128)))