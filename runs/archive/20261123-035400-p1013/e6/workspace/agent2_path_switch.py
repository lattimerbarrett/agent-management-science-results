"""Executable verification of the two-switch endpoint-path map.
For Hamilton path P=x...u-t...y, produces Hamilton paths u...y.
Both topological switch cases are implemented, not just counted.
"""
import itertools, random
import networkx as nx

def switches(G,P,j):
    x=P[0];u=P[j];t=P[j+1]
    out=[]
    # Q=x...u: cut a-b, add x-b and t-a.
    for i in range(j):
        a,b=P[i:i+2]
        if G.has_edge(x,b) and G.has_edge(t,a):
            out.append((tuple(reversed(P[i+1:j+1]))+tuple(P[:i+1])+tuple(P[j+1:]),'Q',i))
    # R=t...y: cut a-b, add x-a and t-b.
    for i in range(j+1,len(P)-1):
        a,b=P[i:i+2]
        if G.has_edge(x,a) and G.has_edge(t,b):
            out.append((tuple(reversed(P[:j+1]))+tuple(reversed(P[j+1:i+1]))+tuple(P[i+1:]),'R',i))
    return out

def check():
    random.seed(17)
    graphs=[]
    for n in range(4,8):
        graphs.append(nx.complete_graph(n))
        for _ in range(4):
            G=nx.complete_graph(n)
            es=list(G.edges);random.shuffle(es)
            for e in es:
                if random.random()<.5 and min(G.degree(v) for v in e)>n/2+1:
                    G.remove_edge(*e)
            graphs.append(G)
    paths=maps=checks=0
    for G in graphs:
        n=len(G);inverses={}
        # Fix old x=0; all remaining endpoint/target choices are enumerated.
        for pp in itertools.permutations(range(1,n)):
            P=(0,)+pp
            if not all(G.has_edge(a,b) for a,b in zip(P,P[1:])):continue
            paths+=1
            for j in range(1,n-1):
                outs=switches(G,P,j)
                assert len(outs)>=G.degree(P[0])+G.degree(P[j+1])-n
                checks+=1
                for Q,kind,i in outs:
                    assert len(Q)==n and len(set(Q))==n
                    assert Q[0]==P[j] and Q[-1]==P[-1]
                    assert all(G.has_edge(a,b) for a,b in zip(Q,Q[1:]))
                    inverses[Q]=inverses.get(Q,0)+1
                    maps+=1
        # For fixed old endpoint x=0 and output path Q, each preimage
        # is reconstructed by old t and <=4 incident-edge choices.
        assert max(inverses.values(),default=0)<=8*n
    return dict(graphs=len(graphs),paths=paths,endpoint_tests=checks,switch_maps=maps)

if __name__=='__main__':print(check())
