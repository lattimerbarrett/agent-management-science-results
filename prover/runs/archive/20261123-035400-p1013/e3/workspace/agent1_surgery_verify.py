from itertools import product

def surgery(n,w,a):
    v,u,x,b=0,1,(w+1)%n,(a+1)%n
    old={tuple(sorted((i,(i+1)%n))) for i in range(n)}
    removed={tuple(sorted(e)) for e in [(v,u),(w,x),(a,b)]}
    if len({v,u,w,x,a,b})<6:return None
    if a>w: added=[(v,w),(u,a),(x,b)]
    else: added=[(v,w),(u,b),(x,a)]
    new=(old-removed)|{tuple(sorted(e)) for e in added}
    adj=[[] for _ in range(n)]
    for i,j in new:adj[i].append(j);adj[j].append(i)
    assert all(len(z)==2 for z in adj)
    seen={0};todo=[0]
    while todo:
        z=todo.pop()
        for t in adj[z]:
            if t not in seen:seen.add(t);todo.append(t)
    assert len(seen)==n
    return added

def verify():
    rewires=0
    for n in range(6,31):
        for w in range(2,n-1):
            for a in range(1,n):
                if surgery(n,w,a) is not None:rewires+=1
    for n in range(6,101):
        for w in range(2,n-1):
            ai=[];bi=[]
            for a in range(1,n):
                b=(a+1)%n
                if len({0,1,w,w+1,a,b})<6:continue
                if a>w: ai.append(a);bi.append(b)
                else:ai.append(b);bi.append(a)
            assert len(ai)==len(set(ai)) and len(bi)==len(set(bi))
            assert len(ai)>=n-6
    colors=0
    for n in range(6,9):
        for word in product(range(3),repeat=n):
            A=word[1]
            for w in range(2,n-1):
                B=word[w+1]
                valid=0
                for a in range(1,n):
                    b=(a+1)%n
                    if len({0,1,w,w+1,a,b})<6:continue
                    if a>w: valid+=word[a]!=A and word[b]!=B
                    else:valid+=word[b]!=A and word[a]!=B
                assert valid>=n-word.count(A)-word.count(B)-6
                colors+=1
    return rewires,colors

if __name__=='__main__':print('Verified cycle rewiring and color exclusion bound:',verify())
