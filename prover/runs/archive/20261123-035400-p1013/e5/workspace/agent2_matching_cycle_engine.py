from functools import lru_cache
from fractions import Fraction
import networkx as nx
from agent4_cycle_engine import cycles

@lru_cache(None)
def turan_cycles(parts):
    return cycles(parts)

def edge_count(parts):
    return sum(parts[i]*parts[j] for i in range(len(parts)) for j in range(i+1,len(parts)))

def matching_cycles(parts,part=0,k=None):
    parts=tuple(parts)
    if k is None:k=parts[part]//2
    assert 0<=2*k<=parts[part]
    w=[1]
    for _ in range(k):
        ww=[0]*(len(w)+2)
        for i,c in enumerate(w):
            ww[i]+=c;ww[i+1]+=2*c;ww[i+2]-=2*c
        w=ww
    ans=-edge_count(parts)
    for ell,c in enumerate(w):
        pp=list(parts);pp[part]-=ell;pp=tuple(pp)
        ans+=c*(2*turan_cycles(pp)+edge_count(pp))
    assert ans%2==0
    return ans//2

def brute(G):
    total=0
    for root in G:
        def walk(path):
            ans=0
            for v in G[path[-1]]:
                if v==root and len(path)>=3:ans+=1
                elif v>root and v not in path:ans+=walk(path+[v])
            return ans
        total+=walk([root])
    return total//2

if __name__=='__main__':
    for pp,k in [((2,2,2),1),((3,2,2),1),((4,2,2),2),((4,3),2)]:
        G=nx.complete_multipartite_graph(*pp)
        G.add_edges_from((2*i,2*i+1) for i in range(k))
        got=matching_cycles(pp,0,k);expected=brute(G)
        assert got==expected,(pp,k,got,expected)
        print('verified',pp,k,got)
