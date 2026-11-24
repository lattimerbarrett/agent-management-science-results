from itertools import combinations, product
from pathlib import Path

def tau(family, ground):
    for z in range(len(ground)+1):
        if any(all(set(c)&f for f in family) for c in combinations(ground,z)):
            return z
    raise ValueError

def construction(t):
    blocks=[]; offset=0
    for i in range(t):
        blocks.append(set(range(offset,offset+i+1))); offset+=i+1
    groups=[]
    for i in range(t):
        groups.append([blocks[i]|set(p) for p in product(*[sorted(x) for x in blocks[i+1:]])])
    return blocks,groups

def check(t):
    blocks,groups=construction(t)
    fs=[f for g in groups for f in g]
    assert all(len(f)==t for f in fs)
    assert all(f&g for f,g in combinations(fs,2))
    assert all(not (x&y) for x,y in combinations(blocks,2))
    assert all(x<=f for x,g in zip(blocks,groups) for f in g)
    ground=sorted(set.union(*blocks))
    assert tau(fs,ground)==t
    # Check inherited exact covering numbers for all class subunions.
    for s in range(1,t+1):
        for I in combinations(range(t),s):
            assert tau([f for i in I for f in groups[i]],ground)==s
    return len(fs),sum(t-len(x) for x in blocks)

for t in range(2,5): print(t,check(t))
# Exact threshold from the elementary pruning bound: if D=sum deficits,
# retaining m classes with deficits <=r forces m<=r*r+r+1.
# Hence D >= (t-r*r-r-1)*(r+1) whenever the parenthesis is positive.
for t in [10,100,1000,10000,1000000]:
    candidates=[((t-r*r-r-1)*(r+1),r) for r in range(int(t**.5)+1)]
    d,r=max(candidates)
    print('elementary lower',t,d,'cutoff',r,'scaled',d/t**1.5)
Path('workspace/agent1_checks.py').write_text(Path('scratchpad.py').read_text())
