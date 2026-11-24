from itertools import combinations
from agent3_check import k_certificate, shelling, appendable
import json
summary=[]
for n,d in [(5,2),(6,3)]:
    fs=[sum(1<<x for x in c) for c in combinations(range(n),d+1)]
    shellcount=0; extensionchecks=0
    for mask in range(1,1<<len(fs)):
        fam=tuple(sorted(fs[i] for i in range(len(fs)) if mask>>i&1))
        sh=shelling(fam)
        kd=k_certificate(fam,d)
        assert (sh is not None)==(kd is not None),(n,d,fam)
        if sh is not None:
            shellcount+=1
            for f in fs:
                if f not in fam:
                    enlarged=tuple(sorted(fam+(f,)))
                    assert (shelling(enlarged) is not None)==appendable(fam,f)
                    extensionchecks+=1
    result={'n':n,'d':d,'families':2**len(fs)-1,'shellable':shellcount,'one_facet_checks':extensionchecks}
    summary.append(result)
    print(result,flush=True)
