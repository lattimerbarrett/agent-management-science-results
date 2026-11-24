from itertools import product
from collections import Counter
from pathlib import Path
T=[(kind,c) for kind in ['C','A','B'] for c in range(3)]
def edge(x,y):
    k,c=x; l,d=y
    if k==l=='C':return c!=d
    return c==d and {k,l} in [{'A','B'},{'C','B'}]
for n in [3,5]:
    hist=Counter()
    for word in product(T,repeat=n):
        if not all(edge(word[i],word[(i+1)%n]) for i in range(n)):continue
        f=sum(word[i][0]==word[(i+1)%n][0]=='C' for i in range(n))
        hist[f]+=1
        if not all(x[0]=='C' for x in word):
            assert n==5 and f==3
            # Exactly one reservoir vertex, type B, between equal-color cores.
            bs=[i for i in range(n) if word[i][0]!='C']
            assert len(bs)==1 and word[bs[0]][0]=='B'
            i=bs[0]
            assert word[(i-1)%n][1]==word[(i+1)%n][1]
    print('cycle length',n,'type-word counts by number of F edges:',dict(hist))
Path('workspace/agent2_cycle_type_check.py').write_text(Path(__file__).read_text())
