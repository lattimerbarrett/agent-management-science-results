from itertools import combinations
import json

def check(n,q):
    facets=[sum(1<<v for v in f) for f in combinations(range(n),q)]
    m=len(facets)
    # Each entry lists other facets' intersections with facet f.
    inter=[[x&y for y in facets] for x in facets]
    def attaches(mask,j):
        if mask==0: return True
        faces={inter[j][i] for i in range(m) if mask>>i&1}
        maximal=[a for a in faces if not any(a!=b and a&b==a for b in faces)]
        return all(a.bit_count()==q-1 for a in maximal)
    shellable=[False]*(1<<m)
    shellable[0]=True
    for mask in range(1,1<<m):
        for j in range(m):
            if mask>>j&1 and shellable[mask^(1<<j)] and attaches(mask^(1<<j),j):
                shellable[mask]=True
                break
    checked=0
    for mask in range(1,1<<m):
        if not shellable[mask]:continue
        for j in range(m):
            if mask>>j&1:
                prev=mask^(1<<j)
                if prev:
                    assert attaches(prev,j), (n,q,mask,j)
                    checked+=1
    return dict(n=n,dimension=q-1,facets=m,shellable_nonempty=sum(shellable)-1,checked_facet_removals=checked)

if __name__=='__main__':
    results=[check(5,3),check(6,4)]
    print(json.dumps(results,indent=2))
    with open('workspace/agent3_append_checks.json','w') as out:json.dump(results,out,indent=2)
    with open('workspace/agent3_append_checks.py','w') as out:out.write(open(__file__).read())
