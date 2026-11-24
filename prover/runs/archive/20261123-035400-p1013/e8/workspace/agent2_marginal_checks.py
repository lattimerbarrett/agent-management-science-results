"""Exact finite checks of the coarse cycle-marginal switching proof."""
from itertools import product
import networkx as nx

def check():
    word_checks=0
    for r in range(3,9):
        for A in range(r):
            for B in range(r):
                if A==B: continue
                for w in product(range(r),repeat=4):
                    if all(w[i]!=w[i+1] for i in range(3)):
                        assert any(w[i]!=B and w[i+1]!=A for i in range(3))
                        word_checks+=1
    switches=0
    for n in range(5,35):
        for j in range(2,n-1):
            G=nx.cycle_graph(n)
            G.remove_edges_from([(0,1),(j,(j+1)%n)])
            G.add_edges_from([(0,j),(1,(j+1)%n)])
            assert nx.is_connected(G) and all(d==2 for _,d in G.degree())
            switches+=1
        for v in range(2,n-1):
            u=0;a=1;b=v+1
            for x in range(n):
                y=(x+1)%n
                if {x,y}&{u,v,a,b}:continue
                G=nx.cycle_graph(n)
                G.remove_edges_from([(u,a),(v,b),(x,y)])
                if 1<=x<v:
                    G.add_edges_from([(u,v),(a,y),(b,x)])
                else:
                    G.add_edges_from([(u,v),(a,x),(b,y)])
                assert len(G.edges())==n
                assert nx.is_connected(G) and all(d==2 for _,d in G.degree())
                switches+=1
    return word_checks,switches
if __name__=='__main__':print('word and switch checks:',check())
