from itertools import combinations
from functools import lru_cache

def maximal(fs):
    fs=set(fs)
    return frozenset(f for f in fs if not any(f<g for g in fs))
@lru_cache(None)
def shell(fs):
    if len(fs)==1:return tuple(fs)
    d=len(next(iter(fs)))-1
    for f in fs:
        rest=fs-{f}
        inter=maximal(f&g for g in rest)
        if all(len(h)==d for h in inter):
            order=shell(rest)
            if order is not None:return order+(f,)
    return None

def report(fs,F):
    inter=maximal(f&F for f in fs)
    print('Gamma facets:',[sorted(f) for f in fs], 'F:',sorted(F))
    print('intersection facets:',[sorted(f) for f in inter])
    for tau in inter:
        if len(tau)<len(F)-1:
            old=maximal(f-tau for f in fs if tau<=f)
            new=F-tau
            print('maximal low-dimensional tau:',sorted(tau))
            print('old link facets:',[sorted(f) for f in old], 'new link simplex:',sorted(new))
            print('common link vertices:',sorted(set().union(*old)&new))
    print('Gamma shelling:',shell(fs))
    print('enlarged shelling:',shell(fs|{F}))

report(frozenset([frozenset('abc'),frozenset('ade')]),frozenset('bcd'))
allf=[frozenset(c) for c in combinations(range(5),3)]
found=False
for mask in range(1,1<<len(allf)):
    fs=frozenset(f for i,f in enumerate(allf) if mask>>i&1)
    for F in allf:
        if F in fs:continue
        if shell(fs|{F}) is not None and shell(fs) is None:
            print('\nA pure nonshellable complex made shellable by one facet:')
            report(fs,F)
            found=True;break
    if found:break
print('found:',found)
