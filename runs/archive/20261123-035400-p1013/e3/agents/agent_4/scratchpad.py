from pathlib import Path
Path('workspace/agent4_H47_exact_extremal_structure.md').write_text(r'''# Exact edge-extremal structure of the checked counter-diagnostic H47

Assume the high-minimum-degree cleanup (proved by progressive induction and
ordinary chi=3 stability in Slack #316/#318). Hence all sufficiently large
edge-extremizers have parts A,B of sizes n/2+O_H(1), bounded cross defect,
and one part A contains a matching covering all but O_H(1) vertices.
All remaining exceptional structure is bounded. The independently checked
positive H-embedding certificates imply:

1. G[A],G[B] are 2P3-free.
2. Delta(G[A])<=5, Delta(G[B])<=3.
3. If A has a P3, B has no P3 and has at most two edges, EVEN allowing
   arbitrary missing cross edges between the chosen rare patterns.
4. If A is a matching, e(G[B])<=7 (22 actual injective certificates in
   agent4_H47_B8_certificates.json plus the connected-size lemma below).
5. H embeds in K5 in A plus two B edges, even with any ONE cross edge
   between those rare vertices absent. Certificate:
   agent4_H47_K5_B2_onehole_certificate.json. By symmetry it covers every
   rare-to-rare one-hole placement. A hole touching an anonymous core
   vertex can instead be avoided by choosing fresh matching/isolate
   fillers. Thus any profile with A containing K5, B containing two
   edges, and total cross holes <=1 contains H.
6. H embeds in K5-e in A plus two B edges, cross complete. Certificate:
   agent4_H47_K5minuse_B2_certificate.json.

## Connected-size lemma

If connected F is 2P3-free and Delta(F)<=D, then |F|<=2D+1.
Take a spanning tree T. Its subtrees isomorphic to P3 pairwise intersect,
so the subtree Helly property gives a vertex x in all of them. Components
of T-x consequently have order <=2, proving |F|<=1+2deg_T(x)<=2D+1.
There is at most one nonmatching connected component in any 2P3-free graph.

For D=3, order 7 forces T to be the subdivided 3-star. Any extra edge
between different arms creates a P3 avoiding the third arm, disjoint from
the third arm together with x. An extra x-leaf edge violates Delta<=3.
Hence F is exactly that tree, with six edges. For |F|<=6, e(F)<=3|F|/2.
Thus every connected 2P3-free Delta<=3 graph has
    e(F)-floor(|F|/2)<=6.
(The full 21-type atlas certificate is needed for the sharper B-total<=7.)

## Primary excess classification

Write u=e(G[A])-floor(|A|/2). Since there is only one nonmatching component
F, the remainder is matching plus isolates. If Delta(F)=5, choose v of
degree 5. F-v is P3-free, or a P3 outside v and two unused neighbors of v
would give two disjoint P3s. Therefore e(F)<=5+floor((|F|-1)/2), so u<=5.

If Delta(F)=4, choose v degree 4. Every P3 in F-v must be entirely inside
N(v), since otherwise at least two neighbors of v lie outside it. Hence
any F-v component meeting V(F)\N[v] has order at most two. By connectivity
such components are single edges linking one neighbor of v to an outside
vertex. Let k be their number. Those k neighbors have no other F-v edges;
all remaining edges lie in the other 4-k neighbors. Thus
    |F|=5+k,
    e(F)<=4+k+binom(4-k,2).
For k>=1 this gives excess <=5. For k=0, F is a graph on five vertices.
Thus excess >=7 occurs only for K5-e (excess 7) or K5 (excess 8).
The Delta<=3 case above has excess <=6.

Consequently:
- if |A| is odd, u<=8; u=8 forces K5 plus a maximum matching;
  u=7 forces K5-e plus a maximum matching, or K5 plus a matching deficient
  by one edge (two additional isolated vertices).
- if |A| is even, u<=7; u=7 forces K5 plus a maximum matching and one
  necessary isolated vertex.

## Exact optimization for n=4k+2

Put m=n/2=2k+1 and |A|=m+x. If B is nonmatching then A is a matching and
    e(G)<=t2(n)+k+7,
because -x^2+floor((x+1)/2)<=0. The checked H-free graph S has
    A=K5 +(k-2)K2, B=K2 +(m-2) isolated vertices,
    e(S)=t2(n)+k+9.
Therefore every edge-extremizer has A nonmatching, B a matching f<=2.
Let M be the total number of missing cross edges. Exactly
    e(G)-t2(n)-k = -x^2+floor((x+1)/2)+u+f-M.
For |x|>=2 the right side is at most 7. For x=-1 it is at most 8. For
x=1, reaching 9 requires u=7,f=2,M=0, hence A contains K5 and H appears.
Thus x=0 for an edge-extremizer.

At x=0, reaching at least 9 leaves only:
- u=8,f=1,M=0: exactly S;
- u=8,f=2,M<=1: excluded by certificate 5;
- u=7,f=2,M=0: excluded by certificate 5 or 6.
Hence for all sufficiently large n=4k+2,
    ex(n,H)=t2(n)+k+9,
and EVERY edge-extremizer is isomorphic to S.

The independently checked H-free T has A=kK2+one isolated vertex and
B=K4+K2+(m-6) isolates. Its cycle count exceeds S for all sufficiently
large k, by the exact cycle-transfer/Bessel first-order computation already
checked by agent3. Thus a=1/4 satisfies the defining properties of S_2
for this H, contradicting the supplied claimed boundary 1/3 if all finite
certificates and the cleanup argument retain their audited validity.
''')
print('Wrote exact-extremal counter-diagnostic proof')
