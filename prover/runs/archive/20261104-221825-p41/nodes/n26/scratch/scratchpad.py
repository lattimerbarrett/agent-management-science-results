from itertools import combinations
from pathlib import Path

def faces(fs):
    return {frozenset(g) for f in fs for r in range(len(f)+1) for g in combinations(f,r)}
def link(C,s):
    return {g-s for g in C if s<=g}
Gamma=faces([frozenset({0,1,2}),frozenset({0,1,3})])
F=frozenset({2,3,4})
I=Gamma & faces([F])
maximal=[s for s in I if not any(s<t for t in I)]
print('maximal intersection faces:',maximal)
for s in maximal:
    Lold=link(Gamma,s); Lnew=faces([F-s]); L=link(Gamma|faces([F]),s)
    print('face',s,'old link',Lold,'new link',Lnew,'actual link',L)
    print('intersection of link vertex sets:',set().union(*Lold)&set().union(*Lnew))
print('Available experiments:',[str(p) for p in Path('experiments').glob('*')])
for name in ['e2','e3']:
    p=Path('experiments')/name/'workspace'
    print(name,'files:',[x.name for x in p.glob('*standalone*')], [x.name for x in p.glob('*universal*')])
