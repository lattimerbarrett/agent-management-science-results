# Matching-cut uncrossing

Let S,T be vertex sets of any graph Q, with both cut edge sets delta(S)
and delta(T) matchings. Write V_ij={v:1_S(v)=i,1_T(v)=j}.

The cut delta(S intersection T) consists edges between V_11 and its
complement. Each vertex of V_10 has at most one neighbor in V_11, since
all such edges lie in the matching delta(T). Likewise each V_01 vertex
has at most one such neighbor using delta(S). A V_00 vertex has at most
one V_11 neighbor since all such edges belong to both matching cuts.
Every V_11 vertex has at most two neighbors outside V_11: each edge must
belong to at least one of the two input matching cuts. Thus degree-2
vertices of the output cut are all in V_11, and their cut-neighbors all
have degree 1. Every nontrivial component is consequently K2 or P3.
The same proof by complement gives the union-cut conclusion.

Verified on all 7601 pairs of matching cuts across graph-atlas graphs
of order <=5: agent4_uncross_verify.py.

Application setup: if chi(H)=3 and H-v is bipartite, fix proper coloring
sigma:H-v -> {0,1}. Every other 2-coloring is tau=sigma xor 1_S.
Monochromatic edges of tau on H-v are exactly delta(S). For an edge
xy with sigma(x)=0, sigma(y)=1:
- x in S,y notin S gives a monochromatic color-1 edge;
- x notin S,y in S gives a monochromatic color-0 edge.
Thus the primary/secondary weighted defect objective is a directed-cut
objective on Q, plus unary costs for edges incident with critical v.

This establishes the source of P3 components and density 2/3 under
uncrossing matching defects, but DOES NOT YET establish the needed
weighted profile exchange theorem. Keeping track of output defect colors,
critical-vertex unary terms, and bounded-gadget wedge statistics remains
unresolved. No assertion that this proves the r=2 universal half.
