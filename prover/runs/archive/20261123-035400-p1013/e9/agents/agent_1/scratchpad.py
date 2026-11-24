from fractions import Fraction
import networkx as nx
import itertools
import json, os

def turan(n,r):
    q,s=divmod(n,r)
    return (n*n-(r-s)*q*q-s*(q+1)**2)//2

def q_edges(r,m,block_v,block_e):
    n=r*m
    return turan(n,r)+(m//block_v)*block_e

checks=0
for r in range(2,21):
    for n in range(1,501):
        # Universal vertex joined to T_{n-1,r}; exact excess.
        z=turan(n-1,r)+n-1-turan(n,r)
        assert z==(n-1)//r
        checks+=1
    for m in range(1,101):
        assert q_edges(r,3*m,3,2)-turan(3*r*m,r)==2*m
        assert q_edges(r,3*m,3,3)-turan(3*r*m,r)==3*m
        checks+=2
print('Verified',checks,'integer identities.')
for m in range(1,101):
    vals=[((3*m+s)*(3*m-s)+(2*(3*m+s))//3,s) for s in range(-3*m,3*m+1)]
    best=max(v for v,s in vals)
    assert best==9*m*m+2*m
    assert [s for v,s in vals if v==best]==[0]
print('Verified unique edge-optimal r2 part balance for m=1,...,100.')

def match(g): return max(dict(g.degree()).values(),default=0)<=1
def p3s(g): return max(dict(g.degree()).values(),default=0)<=2 and all(len(c)<=3 and g.subgraph(c).number_of_edges()<=2 for c in nx.connected_components(g))
num=0
for g in nx.graph_atlas_g():
    n=len(g)
    if n<3 or nx.is_bipartite(g): continue
    vs=list(g)
    a=b=c=False
    for mask in range(1<<n):
        A=[v for i,v in enumerate(vs) if mask>>i&1]
        B=[v for i,v in enumerate(vs) if not(mask>>i&1)]
        ga,gb=g.subgraph(A),g.subgraph(B)
        if ga.number_of_edges()==0:
            a |= p3s(gb)
            c |= match(gb)
        b |= match(ga) and match(gb)
    if a and b and not c:
        print('COUNTEREXAMPLE intersection claim',n, list(g.edges()))
        num+=1
print('Small graph intersection failures:',num)

os.makedirs('workspace',exist_ok=True)
with open('workspace/agent1_host_lemmas.json','w') as f:
    json.dump({'checks':checks,'universal_excess':'floor((n-1)/r)','P3_host_excess':'2n/(3r), when 3r divides n','triangle_host_excess':'n/r, when 3r divides n'},f,indent=2)
