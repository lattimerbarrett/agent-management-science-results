# General endpoint construction (r>=3), independently assembled

Fix s=6 for r=3, s=8 for r=4, and s=2r+1 for r>=5. Put alpha=(s-1)/s and b=alpha/r. Fix K>=2 and L=Ks.

## Hereditary target
S consists of star forests whose components have order at most L, with at most one component of order>s. P consists of linear forests for which sum of orders of components having order>s is at most L-1. Let C=S union P. Require at most one of the r joined parts to have any edge, and that part's internal graph belong to C.

Explicit finite forbidden family: all trees of order L+1; cycles C3,...,C_(L+1); all non-star non-path trees of order at most L; claw disjoint-union P4; two disjoint K_(1,s); and all unions of paths with individual orders>=s+1 and total order in [L,2L-1]. The last bound follows by taking a shortest prefix whose sum reaches L. All forbidden graphs have chromatic number<=3. Add forbidden r-tuples consisting of an edge in each of two different parts. This family is exactly complementary to the target class (after the first two families every component is a tree of order<=L; then shape and capacity constraints are immediate).

## Realization lemma input
For r>=3, the tensor-CSP lemma gives fixed H with chi(H)=r+1 such that a complete join of r bounded-component internal graphs is H-free iff it satisfies the preceding target, up to permutation of parts. Choose hard cluster size M>rL. Include the star obstruction row to ensure H has a vertex whose deletion is r-colorable. Every forbidden-tuple host contains H by the direct intended assignment, with no bounded-component assumption; hence the usual bounded-component core automatically has component order<=L. Include the long-path obstruction to ensure H is a subgraph of P_t join T_((r-1)t,r-1) for some fixed t.

## Global edge structure input
Apply Simonovits bounded-block decomposition theorem to edge-extremizers. Outside O_H(1) exceptional vertices, they are a complete join of r bounded-component symmetric classes, each of size n/r+O_H(1). The direct forbidden-host embeddings force the core into C with at most one active part. Thus core internal edges <=alpha*n/r+O_H(1). Since H has a critical vertex, each exceptional vertex has O_H(1) neighbors in some core class (otherwise greedily embed H through it). This gives ex(n,H)<=t_r(n)+bn+O_H(1).

Conversely balanced joins with packed s-stars are H-free by the CSP reverse implication and give t_r(n)+bn-O_H(1). Therefore the deletion inequality gives delta(G)>= (1-1/r)n-O_H(1) for every edge-extremizer. Assign each exceptional vertex to a class in which it has O_H(1) neighbors. It then has O_H(1) missing cross neighbors. Any forbidden tuple in the full internal parts embeds H using its vertices as fixed soft ports and choosing all remaining vertices greedily from clean core clusters. Hence full internal parts belong to the target class. Fill all missing cross edges: the resulting join is H-free by CSP. Edge maximality forces no missing cross edge. Thus all large edge-extremizers are actual complete joins in the target class.

## Edge optimization when rs divides n
Let m=n/r, with s dividing m. For large u,
E_S(u)=u-1-ceil((u-L)/s),
E_P(u)=u-1-ceil((u-L+1)/s).
At u=m, E_S=m*alpha+K-1 and E_P=E_S-1. S has unique internal maximizer: one star of order L, with all other components order s. For decorated-part shift d, S internal gain is d-ceil(d/s), while the cross-edge loss is Q/2, where Q=sum x_i^2>=2|d| (if d nonzero). This is strictly negative for d!=0. If d=0 but other shifts nonzero the cross loss is positive. Since E_P(u)<=E_S(u) everywhere, S balanced is the unique edge-extremal type.

Consider instead P at decorated size m+1, one other part size m-1, all others m. Use one path of order L-1, a path of order2, and remaining paths of order s. Its internal edge count equals E_S(m), and its total edge count is exactly one less than the extremal count.

## Cycle comparison input
For two joined bounded-degree graphs with fixed part shifts x_i, leading internal edge density alpha_i, bounded edge difference DeltaE, and wedge density difference Delta beta_i, the contraction/Edgeworth lemma gives
n log(c_B/c_A) -> 2r DeltaE/(r-1) - r DeltaQ/(r-2) + 4r sum alpha_i Delta x_i/((r-1)(r-2)) - 2r sum Delta beta_i/(r-1)^2.
Here DeltaE=0, DeltaQ=2, sum alpha_i Delta x_i=alpha, and Delta beta=-(s-2)(s-3)/(2s). Hence limit is
D(r,s)=-2r/(r-2)+4r(s-1)/((r-1)(r-2)s)+r(s-2)(s-3)/((r-1)^2*s).
It is positive for (r,s)=(3,6) and for r>=5,s=2r+1. Thus the edge-minus-one path graph has strictly more cycles than every edge-extremizer, for every sufficiently large n divisible by rs.

For r=4,s=8 this coefficient is zero. With L=Ks fixed first, the coefficient of n^-2 in log(c_P/c_S) is polynomial A K^2+B K+C, with A=r^2*s^2/(r-1)^2>0. All K^2 terms arise from the bounded large star's wedge excess; edge offsets are common and affect the difference only linearly in K, and higher internal moments first enter at n^-3. Taking one sufficiently large fixed K makes the path graph win eventually. This gives the closed endpoint b4.

The unproved/external inputs in this write-up are precisely the tensor-CSP lemma (proved by agents1/3/4), the standard Simonovits bounded-block edge theorem, and the cycle contraction/Edgeworth asymptotics (agent3). It does not address the universal a<b direction's cycle-structure reduction.
