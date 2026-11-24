from pathlib import Path
code='''"""Exact exceptional colorful-tree certificates, no external dependencies."""
from functools import lru_cache
from itertools import combinations

def partitions3(n):
    out=[]
    def visit(word,last):
        if len(word)==n:
            if last==2:
                out.append(tuple(sum(1<<i for i,x in enumerate(word) if x==j) for j in range(3)))
            return
        for x in range(min(last+1,2)+1):visit(word+[x],max(last,x))
    visit([0],0)
    return out

def swaps11():
    base=(15,240,1792) # blocks {0,1,2,3},{4,5,6,7},{8,9,10}
    out={tuple(sorted(base))}
    for u,v in combinations(range(11),2):
        P=list(base)
        a=next(j for j,g in enumerate(P) if g>>u&1)
        b=next(j for j,g in enumerate(P) if g>>v&1)
        if a!=b:
            P[a]^=(1<<u)|(1<<v);P[b]^=(1<<u)|(1<<v)
        out.add(tuple(sorted(P)))
    return sorted(out)

def tree_count(n,parts):
    full=(1<<n)-1
    small=[sum(1<<x for x in C) for C in combinations(range(n),n//2) if 0 in C]
    assert all(A&B for A in small for B in small)
    assert all((full^A)&(full^B) for A in small for B in small)
    assert all(A&(full^B) for A in small for B in small if A!=B)
    masks=[tuple(sum(1<<i for i,P in enumerate(parts) if all(C&g for g in P)) for C in (A,full^A)) for A in small]
    @lru_cache(None)
    def count(k,state):
        assert state
        if k==len(small):return 1
        x,y=masks[k];a,b=x&state,y&state
        if a and b:return count(k+1,a)+count(k+1,b)
        return count(k+1,state)
    result=count(0,(1<<len(parts))-1)
    return result,count.cache_info().currsize

def check():
    expected={8:1556341,9:234983774257,11:70147797197254365921174683698968834468206262353920}
    results={}
    for n in expected:
        parts=swaps11() if n==11 else partitions3(n)
        ans,states=tree_count(n,parts)
        assert ans==expected[n]
        results[n]=dict(leaves=ans,states=states,partitions=len(parts))
    assert expected[8]>1422564
    assert expected[9]>229809982112
    assert expected[11]>2414682040998**4
    print(results)
    return results
if __name__=='__main__':check()
'''
p=Path('workspace/agent4_trees.py');p.write_text(code);exec(compile(code,str(p),'exec'))