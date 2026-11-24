from itertools import combinations
from collections import Counter
out=Counter();examples={}
for n in range(1,8):
    es=list(combinations(range(n),2))
    if len(es)<7:continue
    for inds in combinations(range(len(es)),7):
        deg=[0]*n;masks=[]
        ok=True
        for ix in inds:
            u,v=es[ix];deg[u]+=1;deg[v]+=1
            if deg[u]>3 or deg[v]>3:ok=False;break
            masks.append((1<<u)|(1<<v))
        if not ok or min(deg)==0:continue
        mat3=False
        for i in range(7):
            for j in range(i):
                if masks[i]&masks[j]:continue
                union=masks[i]|masks[j]
                if any(union&masks[k]==0 for k in range(j)):
                    mat3=True;break
            if mat3:break
        if mat3:continue
        t=deg.count(3)
        assert t>=4,(n,[es[i] for i in inds],deg)
        out[n,t]+=1;examples[n,t]=[es[i] for i in inds]
print('All labeled e7 graphs on <=7 nonisolated vertices with Delta<=3 and nu<=2:',dict(out))
print('examples',examples)
import shutil
shutil.copyfile('scratchpad.py','workspace/agent4_subcubic_check.py')
