"""Exact cubic cap verification, with exhaustive labelled degree-sequence enumeration."""
from itertools import combinations
from fractions import Fraction
import networkx as nx
import sympy as sp

def realizations(degrees):
    n=len(degrees); rem=list(degrees); edges=[]
    def rec(i):
        while i<n and rem[i]==0:
            i+=1
        if i==n:
            yield list(edges)
            return
        candidates=[j for j in range(i+1,n) if rem[j]>0]
        d=rem[i]
        if d>len(candidates):
            return
        rem[i]=0
        for S in combinations(candidates,d):
            for j in S: rem[j]-=1
            edges.extend((i,j) for j in S)
            yield from rec(i+1)
            del edges[-d:]
            for j in S: rem[j]+=1
        rem[i]=d
    yield from rec(0)

def resistance_matrix(G, ground):
    vertices=[v for v in G if v!=ground]
    L=sp.Matrix([[G.degree(v) if v==w else -int(G.has_edge(v,w))
                  for w in vertices] for v in vertices])
    return vertices,L.inv()

def verify_caps():
    answer={}
    for n in (5,7):
        reps=[]; count=0
        for edges in realizations([2]+[3]*(n-1)):
            G=nx.Graph();G.add_nodes_from(range(n));G.add_edges_from(edges)
            assert sorted(dict(G.degree()).values())==[2]+[3]*(n-1)
            if not nx.is_connected(G): continue
            count+=1
            if not any(nx.is_isomorphic(G,H) for H in reps): reps.append(G)
        maxima=[]
        for G in reps:
            _,M=resistance_matrix(G,0)
            maxima.append(max(M[i,i] for i in range(n-1)))
        maxima.sort()
        answer[n]=(count,maxima)
    assert answer[5]==(6,[sp.Rational(7,8)])
    assert answer[7]==(810,[sp.Rational(38,39),sp.Rational(104,105),sp.Rational(11,10),sp.Rational(11,8)])
    return answer

if __name__=='__main__':
    print(verify_caps())
