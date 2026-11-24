from functools import lru_cache
from itertools import combinations

def subs(f):
    q=f
    while q:
        yield q
        q=(q-1)&f

def maximal(fs):
    fs=set(fs)
    return frozenset(f for f in fs if not any(f!=g and f&g==f for g in fs))

def deletion(fs,s):
    return maximal([g for f in fs for g in ([f] if f&s!=s else [f^v for v in subs(s) if v.bit_count()==1])])

def link(fs,s):
    return frozenset(f^s for f in fs if f&s==s)

def rank(fs):
    sizes={f.bit_count() for f in fs}
    return next(iter(sizes)) if len(sizes)==1 else None

@lru_cache(None)
def witness(fs,k):
    r=rank(fs)
    if r is None: return None
    if len(fs)==1:return 0
    candidates=set(s for f in fs for s in subs(f) if s.bit_count()<=k+1)
    for s in sorted(candidates,key=lambda x:(x.bit_count(),x)):
        de=deletion(fs,s)
        if rank(de)==r and witness(de,k) is not None and witness(link(fs,s),k) is not None:
            return s
    return None

def prefix_order(fs,k):
    s=witness(fs,k)
    assert s is not None
    if s==0:return list(fs)
    return prefix_order(deletion(fs,s),k)+[f|s for f in prefix_order(link(fs,s),k)]

def skeleton(fs,r):
    return frozenset(s for f in fs for s in subs(f) if s.bit_count()==r)

def check():
    count=0
    for n in range(1,6):
      for r in range(1,n+1):
       allfs=[sum(1<<v for v in c) for c in combinations(range(n),r)]
       for flags in range(1,1<<len(allfs)):
        fs=frozenset(f for i,f in enumerate(allfs) if flags>>i&1)
        for k in range(0,3):
         if witness(fs,k) is None:continue
         count+=1
         order=prefix_order(fs,k)
         for j in range(1,len(order)+1):assert witness(frozenset(order[:j]),k) is not None
         for q in range(1,r+1):assert witness(skeleton(fs,q),k) is not None
         for s in set(s for f in fs for s in subs(f)):
             assert witness(link(fs,s),k) is not None
         a=1<<n
         if r>1:
          order2=prefix_order(skeleton(fs,r-1),k)
          for j in range(1,len(order2)+1):
             assert witness(fs|frozenset(a|f for f in order2[:j]),k) is not None
         for x in [1<<v for v in range(n) if any(f>>v&1 for f in fs)]:
          lk=link(fs,x)
          new=fs|frozenset(a|f for f in lk)
          assert witness(new,k) is not None
          assert witness(deletion(new,x),k) is not None
    return count
