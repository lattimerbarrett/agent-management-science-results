from itertools import product, combinations
from collections import defaultdict

def add(*terms):
    out=defaultdict(int)
    for a in terms:
        for w,v in a.items(): out[w]+=v
    return {w:v for w,v in out.items() if v}

def scale(a,c): return {w:c*v for w,v in a.items() if c*v}

def mul(a,b):
    out=defaultdict(int)
    for u,x in a.items():
        for v,y in b.items(): out[u+v]+=x*y
    return {w:v for w,v in out.items() if v}

def bracket(a,b): return add(mul(a,b),scale(mul(b,a),-1))

def deriv(D,a):
    out=defaultdict(int)
    for w,c in a.items():
        for k,i in enumerate(w):
            for v,d in D.get(i,{}).items(): out[w[:k]+v+w[k+1:]]+=c*d
    return {w:c for w,c in out.items() if c}

def dbracket(D,E):
    out={}
    for i in D.keys()|E.keys():
        v=add(deriv(D,E.get(i,{})),scale(deriv(E,D.get(i,{})),-1))
        if v: out[i]=v
    return out

def flatten(D,n):
    return {(i,)+w:c for i,a in D.items() for w,c in a.items()}

def elementary(n):
    return [((i,j,k),{i:{(j,k):1,(k,j):-1}}) for i in range(n) for j in range(n) for k in range(j+1,n)]

def sparse_rank(columns,p):
    piv={}
    for col in columns:
        col={w:c%p for w,c in col.items() if c%p}
        while col:
            r=min(col)
            if r not in piv:
                inv=pow(col[r],-1,p)
                piv[r]={w:c*inv%p for w,c in col.items()}
                break
            q=col[r]; pc=piv[r]
            for w,c in pc.items():
                v=(col.get(w,0)-q*c)%p
                if v: col[w]=v
                else: col.pop(w,None)
    return len(piv)

def degree2_columns(n):
    gens=elementary(n)
    return [flatten(dbracket(D,E),n) for (_,D),(_,E) in combinations(gens,2)]

if __name__=='__main__':
    import json
    results=[]
    for n in range(2,8):
        cols=degree2_columns(n)
        expected=n*n*(n*n-1)//3-n*(n+1)//2
        ranks={p:sparse_rank(cols,p) for p in [2,3,5,101]}
        assert all(v==expected for v in ranks.values())
        results.append(dict(n=n,generators=len(elementary(n)),bracket_columns=len(cols),ranks=ranks,expected=expected))
        print(results[-1],flush=True)
    open('workspace/agent2_degree2_results.json','w').write(json.dumps(results,indent=2))
