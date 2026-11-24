from functools import lru_cache
from math import factorial
from fractions import Fraction

def paths(parts,s,t):
    cap=list(parts);cap[s]-=1;cap[t]-=1
    @lru_cache(None)
    def rec(rem,last,used):
        z=int(last!=t and used>=1)
        for j,k in enumerate(rem):
            if j!=last and k:
                rr=list(rem);rr[j]-=1
                z+=k*rec(tuple(rr),j,used+1)
        return z
    return rec(tuple(cap),s,0)

def cycles(parts):
    # Partition cycles by smallest labelled vertex. Delete it and count paths among its neighbors.
    p=list(parts); total=0
    for s in range(len(p)):
        while p[s]:
            p[s]-=1
            for i in range(len(p)):
                if i==s:continue
                for j in range(i,len(p)):
                    if j==s:continue
                    if i==j and p[i]>=2:
                        total+=p[i]*(p[i]-1)//2*paths(p,i,j)
                    elif i!=j and p[i] and p[j]:
                        total+=p[i]*p[j]*(paths(p,i,j)+1) # direct path valid triangle
    return total

def path_systems(parts,pairs):
    cap=list(parts)
    for a,b in pairs:cap[a]-=1;cap[b]-=1
    if min(cap)<0:return 0
    @lru_cache(None)
    def rec(rem,j,last):
        end=pairs[j][1]
        z=0
        if last!=end:
            if j+1==len(pairs):z=int(sum(rem)==0)
            else:z=rec(rem,j+1,pairs[j+1][0])
        for i,k in enumerate(rem):
            if i!=last and k:
                rr=list(rem);rr[i]-=1
                z+=k*rec(tuple(rr),j,i)
        return z
    return rec(tuple(cap),0,pairs[0][0])

def brute_cycles(parts, added=None, deleted=None):
    import networkx as nx
    G=nx.complete_multipartite_graph(*parts)
    if added:G.add_edge(*added)
    if deleted:G.remove_edge(*deleted)
    z=0
    for root in G:
        def walk(path):
            out=0
            for v in G[path[-1]]:
                if v==root and len(path)>=3:out+=1
                elif v>root and v not in path:out+=walk(path+[v])
            return out
        z+=walk([root])
    assert z%2==0
    return z//2

if __name__=='__main__':
    for p in [(2,2),(3,2),(2,2,2),(3,2,2),(3,3,2)]:
        c=cycles(p); a=paths(p,0,0);b=paths(p,0,1)
        bc=brute_cycles(p)
        assert c==bc,(p,c,bc)
        assert a==brute_cycles(p,added=(0,1))-bc
        assert b==bc-brute_cycles(p,deleted=(0,p[0]))
        print('brute verified',p,c,a,b)
    for m in range(2,14):
        p=(m,)*3;c=cycles(p);a=paths(p,0,0);b=paths(p,0,1)
        print(m, float(Fraction(3*m*a,c)),float(Fraction(3*m*b,c)),float(Fraction(a,b)),flush=True)
    for m in [5,10,15,20,30]:
        cb=cycles((m,m,m));cu=cycles((m+1,m-1,m))
        print('imbalance normalized coefficient',m,float(Fraction(3*m*(cb-cu),2*cb)))
    for m in [4,6,10,15,20,30]:
        p=(m,)*3
        p00=path_systems(p,[(0,0),(0,0)])
        p01=path_systems(p,[(0,1),(0,1)])
        print('two-path endpoint ratio',m,float(Fraction(p00,p01)))
    import sympy as sp
    for r in [2,3,4]:
        xs=sp.symbols('x:'+str(r));X=sp.diag(*xs);B=sp.ones(r)-sp.eye(r)
        F=B*(sp.eye(r)-X*B).inv()
        D=1-sum(x/(1+x) for x in xs)
        for a in range(r):
            for b in range(r):
                claimed=1/((1+xs[a])*(1+xs[b])*D)-(int(a==b)/(1+xs[a]))
                assert sp.cancel(F[a,b]-claimed)==0
        print('rational path GF identity verified',r)
    from itertools import combinations
    for parts in [(2,2),(3,2),(2,2,2),(3,2,2)]:
        r=len(parts);N=sum(parts);xs=sp.symbols('x:'+str(r))
        P=sum((len(S)-1)*sp.prod(xs[i] for i in S) for s in range(2,r+1) for S in combinations(range(r),s))
        C=sp.Poly(sp.expand(sum(P**l/sp.Integer(2*l) for l in range(1,N//2+1))-sum(xs[i]*xs[j]/2 for i in range(r) for j in range(i+1,r))),*xs)
        z=sp.Rational(0)
        for mon,coef in C.terms():
            if all(a<=b for a,b in zip(mon,parts)):
                z+=coef*sp.prod(sp.Rational(factorial(b),factorial(b-a)) for a,b in zip(mon,parts))
        assert z==cycles(parts),(parts,z,cycles(parts))
        print('full cycle EGF coefficient verified',parts,z)
    import shutil
    shutil.copyfile('scratchpad.py','workspace/agent4_cycle_engine.py')
