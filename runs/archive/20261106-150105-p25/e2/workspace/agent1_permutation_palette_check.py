from pathlib import Path
from itertools import combinations, permutations
from math import factorial
for m in range(3,8):
    triples=list(combinations(range(m),3))
    cnt={t:0 for t in triples}
    comp=[(t,u) for t in triples for u in triples if t[1:]==u[:2]]
    for p in permutations(range(m)):
        I={t for t in triples if p[t[1]]>max(p[t[0]],p[t[2]])}
        for t in I: cnt[t]+=1
        assert all(not (t in I and u in I) for t,u in comp)
    assert all(c==factorial(m)//3 for c in cnt.values())
    print(m,len(triples), 'all permutation palettes independent; exact coverage=',factorial(m)//3,'/',factorial(m))
Path('workspace/agent1_permutation_palette_check.py').write_text(Path('scratchpad.py').read_text())
