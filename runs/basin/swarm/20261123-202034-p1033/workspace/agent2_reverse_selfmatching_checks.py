from itertools import combinations,product
from pathlib import Path
import json

def check(T,L):
    out=[[] for _ in range(T)]
    for i,j in combinations(range(T),2):
        n=T if T%2 else T+1
        a,b=(i,j) if (j-i)%n<=n//2 else (j,i)
        out[a].append(b)
    indeg=[sum(i in out[j] for j in range(T)) for i in range(T)]
    X=[];c=0
    for d in indeg:
        X.append(set(range(c,c+d+1)));c+=d+1
    oldH=[];own=[]
    for i in range(T):
        for p in product(*(sorted(X[j]) for j in out[i])):
            oldH.append(X[i]|set(p));own.append(i)
    # Clone-pack blowup of all old points.
    X=[{L*x+a for x in C for a in range(L)} for C in X]
    H=[{L*x+a for x in F for a in range(L)} for F in oldH]
    qlabel={};nextpoint=0
    for i,C in enumerate(X):
        for x in sorted(C)[1:]:qlabel[i,x]=nextpoint;nextpoint+=1
    copies={};Q=[]
    for F,i in zip(H,own):
        B={p for (j,x),p in qlabel.items() if j==i}
        for x in sorted(F-X[i]):
            if (i,x) not in copies:copies[i,x]=nextpoint;nextpoint+=1
            B.add(copies[i,x])
        assert len(B)==T*L-1
        Q.append(B)
    selfpetals={}
    for (i,x),q in qlabel.items():
        S={q}|{p for (j,y),p in copies.items() if y==x}
        conditional=[B for B,F in zip(Q,H) if x in F]
        assert conditional and all(S&B for B in conditional)
        assert all(any(S&B=={p} for B in conditional) for p in S)
        selfpetals[x]=S
    assert all(not S&R for S,R in combinations(selfpetals.values(),2))
    q=len(selfpetals)
    assert q==sum(map(len,X))-T
    return dict(inner_classes=T,clones=L,inner_edges=len(H),inner_rank=T*L,
                inner_ground=len(set.union(*X)),factored_ground=nextpoint,
                checked_self_petals=q,all_self_pairs=q*(q-1)//2,
                maximum_self_rank=max(map(len,selfpetals.values())),
                target_completion_maxdef_lower=(q-1)/2)
rows=[check(t,L) for t in (3,4,5,6) for L in (1,2,3)]
print(json.dumps(rows,indent=2))
Path('workspace/agent2_reverse_selfmatching_checks.json').write_text(json.dumps(rows,indent=2))
