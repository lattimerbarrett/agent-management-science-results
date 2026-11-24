import itertools, functools,time,json,os
n=8; full=(1<<n)-1
sets=[s for s in range(1<<n) if s.bit_count()==4]
pairs=[(s,full^s) for s in sets if s<(full^s)]
def partitions(n,k):
    def rec(a,m):
        if len(a)==n:
            if m==k-1: yield a
            return
        for j in range(min(m+1,k-1)+1):yield from rec(a+[j],max(m,j))
    for a in rec([0],0):
        yield tuple(sum(1<<i for i,c in enumerate(a) if c==j) for j in range(k))
P=list(partitions(n,3))
def mask(s):return sum(1<<i for i,p in enumerate(P) if all(s&b for b in p))
fixed=(3,28,224)
pairs.sort(key=lambda p:(not all(s&b for s in p for b in fixed),p))
M=[(mask(s),mask(t)) for s,t in pairs]
print('parts',len(P),'pairs',len(M),'balanced',sum(all(s&b for s in p for b in fixed) for p in pairs),flush=True)
nodes=0
@functools.lru_cache(None)
def count(i,V):
    global nodes
    nodes+=1
    if i==len(M):return 1
    a,b=(V&m for m in M[i])
    if not a and not b:return 1
    return (count(i+1,a) if a else 0)+(count(i+1,b) if b else 0)
t=time.time();ans=count(0,(1<<len(P))-1)
print('ans',ans,'nodes',nodes,'time',time.time()-t)
os.makedirs('workspace',exist_ok=True)
open('workspace/agent3_color_tree.py','w').write(open(__file__).read())
json.dump({'answer':ans,'nodes':nodes,'seconds':time.time()-t},open('workspace/agent3_color_tree.json','w'))
