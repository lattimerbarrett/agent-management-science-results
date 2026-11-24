from functools import lru_cache
m=6
subsets=list(range(1<<m))
adj=[]
for a in subsets:
    adj.append(sum(1<<j for j,b in enumerate(subsets) if (a&b)!=a and (a&b)!=b))
@lru_cache(None)
def clique_count(candidates):
    total=1
    while candidates:
        b=candidates&-candidates;candidates^=b
        total+=clique_count(candidates&adj[b.bit_length()-1])
    return total
answer=clique_count((1<<(1<<m))-1)
assert answer==7828354
assert answer+1 <2**24
print('All antichains on six points:',answer)
print('Therefore lambda(7)+1 <=',answer+1,'<',2**24)
print(clique_count.cache_info())
