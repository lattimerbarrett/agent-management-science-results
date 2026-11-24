from itertools import product, combinations
from collections import Counter, deque
from pathlib import Path
code='''from itertools import product, combinations
from collections import Counter, deque

def check_topology(m=7):
    caps=(2,2,2,m-5)
    faces=[]
    for a in product(range(5),repeat=m):
        if all(a.count(i+1)<=caps[i] for i in range(4)):
            faces.append(tuple(4*j+x-1 for j,x in enumerate(a) if x))
    idx={s:i for i,s in enumerate(faces)}
    def match(s):
        occupied={v//4 for v in s if v%4<3}
        p=next(j for j in range(m) if j not in occupied)
        v=4*p+3
        if v in s: return tuple(x for x in s if x!=v)
        if sum(x%4==3 for x in s)<m-5:return tuple(sorted(s+(v,)))
        return None
    adj=[[] for _ in faces]; indeg=[0]*len(faces)
    crit=[]
    for i,s in enumerate(faces):
        t=match(s)
        if t is not None:
            assert match(t)==s and t in idx
        elif s: crit.append(len(s)-1)
        for k in range(len(s)):
            t=s[:k]+s[k+1:];j=idx[t]
            u,v=(j,i) if match(t)==s else (i,j)
            adj[u].append(v); indeg[v]+=1
    q=deque(i for i,d in enumerate(indeg) if not d);seen=0
    while q:
        u=q.popleft();seen+=1
        for v in adj[u]:
            indeg[v]-=1
            if indeg[v]==0:q.append(v)
    assert seen==len(faces), 'Matching has directed cycle'
    assert max(crit)<=m-2
    # Every forbidden triangle in full column join has a cone filling.
    forbidden=0
    for cols in combinations(range(m),3):
        for rows in product(range(4),repeat=3):
            s=tuple(4*c+r for c,r in zip(cols,rows))
            if s in idx:continue
            forbidden+=1
            assert len(set(rows))==1 and caps[rows[0]]==2
            c=next(c for c in range(m) if c not in cols)
            w=4*c+(rows[0]+1)%4
            for edge in combinations(s,2):assert tuple(sorted(edge+(w,))) in idx
    return {'m':m,'faces_including_empty':len(faces),'critical_reduced_dimensions':dict(Counter(crit)),'forbidden_triangles_filled':forbidden}

if __name__=='__main__':print(check_topology())
'''
Path('workspace/a4_topology_check.py').write_text(code)
exec(compile(code,'a4_topology_check.py','exec'))
