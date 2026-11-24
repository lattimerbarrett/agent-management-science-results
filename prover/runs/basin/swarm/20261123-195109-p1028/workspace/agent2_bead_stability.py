"""Finite certificate used in quartic bead stability after monotone-path reduction."""
from itertools import combinations
import networkx as nx
import sympy as sp

def monotone_patterns(max_size=5):
    # Two ordered bipartition parts with degrees 1 on W, 2 otherwise.
    # No strict inversion means its transportation matrix is uniquely given
    # by the northwest-corner rule. Reject entries 2 (multiple edges).
    for r in range(1,max_size+1):
      for s in range(1,max_size+1):
       for k in range(5):
        if r-s!=k-2: continue
        for A in combinations(range(r),k):
         if A and A[-1]-A[0]>2: continue
         for B in combinations(range(s),4-k):
          if B and B[-1]-B[0]>2: continue
          da=[2-int(i in A) for i in range(r)]
          db=[2-int(j in B) for j in range(s)]
          i=j=0; edges=[]; ok=True
          while i<r and j<s:
           v=min(da[i],db[j])
           if v!=1: ok=False; break
           edges.append((i,j)); da[i]-=1;db[j]-=1
           if da[i]==0:i+=1
           if db[j]==0:j+=1
          if ok and i==r and j==s: yield r,s,A,B,edges

def verify_stability():
    counts={};max_excess=None
    for r,s,A,B,edges in monotone_patterns():
        m=r+s+3; u=0;t=r+s+1;w=t+1
        G=nx.Graph();aa=[u]+list(range(1,r+1))+[t]
        bb=[u]+list(range(r+1,r+s+1))+[t]
        G.add_edges_from(zip(aa,aa[1:]));G.add_edges_from(zip(bb,bb[1:]))
        G.add_edges_from((aa[i+1],bb[j+1]) for i,j in edges)
        G.add_edges_from((w,aa[i+1]) for i in A)
        G.add_edges_from((w,bb[j+1]) for j in B)
        assert G.degree(u)==G.degree(t)==2
        assert all(G.degree(v)==4 for v in G if v not in [u,t])
        L=sp.Matrix([[G.degree(v) if v==z else -int(G.has_edge(v,z))
                      for z in range(1,m)] for v in range(1,m)])
        R=L.inv()[t-1,t-1]
        if m==7: assert R==sp.Rational(4,3)
        else: assert R<=sp.Rational(m-2,4)
        counts[m]=counts.get(m,0)+1
    assert counts=={7:1,8:4,9:6,10:4,11:6,12:4,13:2}
    return counts
if __name__=='__main__': print(verify_stability())
