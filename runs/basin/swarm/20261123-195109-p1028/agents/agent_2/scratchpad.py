from pathlib import Path
code='''"""Independent literal large-integer formula and Markov-equation verification."""
import sympy as sp
import math
from fractions import Fraction
from itertools import combinations
import networkx as nx

def check(n):
    N=n*(n-1)//2; D=math.lcm(*range(1,n**(n-2)+1));b=N+1
    pairs=list(combinations(range(n),2));S=0;commutes=[];all_commutes=[];count=0
    for mask in range(1<<N):
        G=nx.Graph();G.add_nodes_from(range(n))
        G.add_edges_from(e for j,e in enumerate(pairs) if (mask>>j)&1)
        ds=[G.degree(i) for i in range(n)]
        L=sp.Matrix([[ds[i] if i==j else -int(G.has_edge(i,j))
                      for j in range(n)] for i in range(n)])
        K=int(L[:n-1,:n-1].det())
        q=1-int(sp.floor(sp.Rational(1,K+1)))
        r=math.prod(int(sp.floor(sp.Rational(1,1+(d-ds[0])**2))) for d in ds[1:])
        if q*r==0: continue
        count+=1
        F=int(L.extract(list(range(2,n)),list(range(2,n))).det())
        e=sp.Rational(n*ds[0]*D*F,K)
        assert e.q==1
        S+=1<<(b*int(e))
        # Independent hitting time solution, not using tree determinants.
        def hitting(target,start):
            vs=[i for i in range(n) if i!=target]
            A=sp.Matrix([[int(i==j)-sp.Rational(int(G.has_edge(i,j)),ds[i])
                          for j in vs] for i in vs])
            h=A.inv()*sp.ones(n-1,1)
            return h[vs.index(start)]
        c=hitting(0,1)+hitting(1,0)
        assert c==sp.Rational(e,D)
        commutes.append(c)
        for u,v in pairs:
            c_uv=hitting(u,v)+hitting(v,u)
            keep=[i for i in range(n) if i not in [u,v]]
            F_uv=int(L.extract(keep,keep).det())
            assert c_uv==sp.Rational(n*ds[0]*F_uv,K)
            all_commutes.append(c_uv)
    answer=Fraction((S.bit_length()-1)//b,D)
    assert answer==max(commutes)==max(all_commutes)
    return dict(n=n,D=D,graphs=count,S_bits=S.bit_length(),answer=str(answer))
if __name__=='__main__':
    for n in (2,3,4): print(check(n))
'''
Path('workspace/agent2_encoding_check.py').write_text(code)
exec(compile(code,'agent2_encoding_check.py','exec'))
