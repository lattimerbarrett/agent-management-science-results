"""Exact cycles for complete bipartite graphs with internal matchings/triangles.
Derivations: contract each internal linear-forest component to an alternating run.
Includes brute force verification for all templates of total order <= 10.
"""
from collections import defaultdict
from math import factorial,comb
from fractions import Fraction
import networkx as nx

POLYS={1:{(0,0):1,(1,1):1},2:{(0,0):1,(1,1):2,(2,2):1,(2,1):2},3:{(0,0):1,(1,1):3,(2,2):3,(2,1):6,(3,3):1,(3,2):6,(3,1):6}}
def triangle_cycles(a,b):
    p={(0,0):1}
    for z in [3]*(a//3)+([a%3] if a%3 else []):
        q=defaultdict(int)
        for (v,k),c in p.items():
            for (w,l),d in POLYS[z].items():q[v+w,k+l]+=c*d
        p=q
    twice=2*(a//3)
    for (v,k),c in p.items():
        if 1<=k<=b and v+k>=3:twice+=c*factorial(k-1)*factorial(b)//factorial(b-k)
    assert twice%2==0
    return twice//2

def matching_cycles(a,b):
    def poly(a):
        d=defaultdict(int)
        for i in range(a//2+1):
            for s in range(a-2*i+1):d[i+s,2*i+s]+=comb(a//2,i)*comb(a-2*i,s)*2**i
        return d
    p,q=poly(a),poly(b)
    twice=0
    for (k,v),c in p.items():
        if not k:continue
        for (l,w),d in q.items():
            if k==l and v+w>=3:twice+=c*d*factorial(k)*factorial(k-1)
    assert twice%2==0
    return twice//2

def template(a,b,kind):
    g=nx.complete_bipartite_graph(a,b)
    if kind=='triangle':
        for x in range(0,a,3):
            for u in range(x,min(x+3,a)):
                for v in range(u+1,min(x+3,a)):g.add_edge(u,v)
    else:
        for start,end in [(0,a),(a,a+b)]:
            for u in range(start,end-1,2):g.add_edge(u,u+1)
    return g

def brute_cycles(g):
    total=0
    for root in g:
        def walk(path,used):
            nonlocal total
            for v in g[path[-1]]:
                if v==root and len(path)>=3:total+=1
                elif v>root and v not in used:walk(path+[v],used|{v})
        walk([root],{root})
    assert total%2==0
    return total//2

def verify():
    cases=0
    for a in range(1,8):
        for b in range(1,8):
            if a+b>10:continue
            for kind,f in [('triangle',triangle_cycles),('matching',matching_cycles)]:
                actual=brute_cycles(template(a,b,kind))
                assert actual==f(a,b),(a,b,kind,actual,f(a,b))
                cases+=1
    # Fully rational strict comparison of the limiting series, using rigorous tail.
    # A= sum4^k/(k!)^2; D=sum3^(k+2)/(k!(k+2)!).
    K=20
    A=sum((Fraction(4**k,factorial(k)**2) for k in range(K+1)),Fraction())
    D=sum((Fraction(3**(k+2),factorial(k)*factorial(k+2)) for k in range(K+1)),Fraction())
    nextD=Fraction(3**(K+3),factorial(K+1)*factorial(K+3))
    ratio=Fraction(3,(K+2)*(K+4))
    assert A>D+nextD/(1-ratio)
    return cases,float(A),float(D)
def universal_gap_certificate(K=20):
    # I_j(2)=sum_{k>=0}1/(k!(k+j)!). All operations rational.
    def partial(j):
        low=sum((Fraction(1,factorial(k)*factorial(k+j)) for k in range(K+1)),Fraction())
        nxt=Fraction(1,factorial(K+1)*factorial(K+1+j))
        ratio=Fraction(1,(K+2)*(K+2+j))
        return low,low+nxt/(1-ratio)
    lowerQ=sum((Fraction(3**k,factorial(k)**2) for k in range(K+1)),Fraction())
    upperU=partial(0)[1]+2*partial(1)[1]+partial(2)[1]
    assert lowerQ>upperU
    return float(lowerQ),float(upperU),float(lowerQ-upperU)

if __name__=='__main__':
    print('verified templates, limiting constants:',verify())
    print('universal gap certified:',universal_gap_certificate())
    for m in [89,95,101,125]:
        x,y=matching_cycles(m,m),triangle_cycles(m+1,m-1)
        print(m,'matching > triangle:',x>y,'ratio:',float(Fraction(x,y)))
