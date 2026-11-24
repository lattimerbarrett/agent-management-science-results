from itertools import combinations
from pathlib import Path

def variable_sets(sizes):
    r=sum(sizes);groups=[];a=0
    for z in sizes:
        groups.append(set(range(a,a+z)));a+=z
    m=r//2
    As=[frozenset(A) for A in combinations(range(r),m) if 0 in A and all(0<len(set(A)&g)<len(g) for g in groups)]
    return groups,As

def orders_from_variables(sizes,n):
    groups,As=variable_sets(sizes);r=sum(sizes)
    # Encode vertex by binary digits. For each coordinate use signed lex order.
    bitlength=(n-1).bit_length(); assert bitlength<=len(As)
    As=As[:bitlength]
    perms=[]
    for j in range(r):
        perms.append(sorted(range(n),key=lambda x:tuple(((x>>b)&1) if j in As[b] else 1-((x>>b)&1) for b in range(bitlength))))
    assert all(any(p.index(v)>p.index(w) and p.index(v)>p.index(x) for p in perms) for v in range(n) for w,x in combinations([z for z in range(n) if z!=v],2))
    for g in groups:
        assert all(any(perms[j].index(v)>perms[j].index(w) for j in g) for v in range(n) for w in range(n) if v!=w)
    return groups,perms

def standard(t):
    el=list(range(2*t))
    le=lambda a,b:a==b or (a<t and b>=t and a!=b-t)
    Ls=[]
    for i in range(t):
        L=[a for a in range(t) if a!=i]+[t+i,i]+[t+a for a in range(t) if a!=i]
        Ls.append(L)
    return el,le,Ls

def check(sizes,n=16):
    t=len(sizes);r=sum(sizes);groups,perms=orders_from_variables(sizes,n)
    P,leP,Ls=standard(t);Q=[(v,) for v in range(n)]+list(combinations(range(n),2))
    E=[(p,A) for p in P for A in Q]
    po=[]
    for j,perm in enumerate(perms):
        i=next(i for i,g in enumerate(groups) if j in g)
        pv={v:z for z,v in enumerate(perm)};pp={p:z for z,p in enumerate(Ls[i])}
        L=sorted(E,key=lambda z:(max(pv[v] for v in z[1]),pp[z[0]],len(z[1]),z[1]))
        po.append({z:k for k,z in enumerate(L)})
    for x in E:
        for y in E:
            actual=leP(x[0],y[0]) and set(x[1])<=set(y[1])
            assert actual==all(p[x]<=p[y] for p in po),(x,y)
    print('verified entire product realizer',sizes,n,len(E),'elements',r,'extensions',flush=True)

if __name__=='__main__':
    for sizes in [(3,3,3),(2,2,3,3),(2,2,2,2,3),(2,2,2,2,2,2)]:
        groups,As=variable_sets(sizes)
        print('variable sets',sizes,len(As),'capacity',2**len(As),flush=True)
        check(sizes)
