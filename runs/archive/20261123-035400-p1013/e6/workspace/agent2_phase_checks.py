"""Finite exact checks accompanying agent2_direct_counterproof.md.
These supplement the symbolic arguments; they are not universal proofs.
"""
from fractions import Fraction as Q
from math import ceil
import networkx as nx


def check_connected_classification():
    fork=nx.Graph([(0,1),(0,2),(0,3),(3,4)])
    checked=0
    for G in nx.graph_atlas_g():
        if not len(G) or not nx.is_connected(G):continue
        if any(nx.triangles(G).values()):continue
        if nx.algorithms.isomorphism.GraphMatcher(G,fork).subgraph_is_monomorphic():continue
        ds=sorted(dict(G.degree()).values())
        star=(len(G)==1 or ds==[1]*(len(G)-1)+[len(G)-1])
        assert star or max(ds)<=2,(nx.to_graph6_bytes(G),ds)
        checked+=1
    return checked


def check_forest_capacity(limit=300):
    # Every ordinary component may have order 1..11. At most one
    # exceptional path has order 12..22. A component of order j has j-1 edges.
    inf=10**9
    dp=[[inf,inf] for _ in range(limit+1)];dp[0][0]=0
    for n in range(1,limit+1):
        for j in range(1,min(11,n)+1):
            for b in [0,1]:dp[n][b]=min(dp[n][b],1+dp[n-j][b])
        for j in range(12,min(22,n)+1):
            dp[n][1]=min(dp[n][1],1+dp[n-j][0])
    for n in range(12,limit+1):
        assert n-min(dp[n])==n-ceil(n/11)+1
    for q in range(2,limit//11+1):
        n=11*q
        opt=min(dp[n])
        # Any maximizing partition has q-1 parts; hence a single part
        # of order exactly22 and all others11, by the capacity sum.
        assert opt==q-1
        assert 22+11*(opt-1)==n
    return limit-11


def check_numeric_inequalities():
    assert 1+Q(1,3)+Q(100,363)<2
    checks=1
    for r in range(3,1001):
        k=2*r+3
        delta=Q((k-2)*(k-3),2*k)-(r-1)
        assert delta==Q(3,k)>0
        assert Q(k-1,k*r)<Q(1,r)
        checks+=1
    return checks

if __name__=='__main__':
    print('connected triangle/fork-free atlas checks:',check_connected_classification())
    print('forest capacity DP checks:',check_forest_capacity())
    print('exact counterphase inequalities:',check_numeric_inequalities())
