# Fully elementary explicit global upper bound for the diagnostic H
Use old labels V(H)={0,1,2,3,4,5,7,8} and E(H)={04,07,08,17,18,27,28,34,35,48,58,78}.
Put f(n)=max_{0<=a<=n}(a(n-a)+floor(2a/3)).
We prove ex(n,H)=f(n) for n>=10^8. No external stability theorem is needed.

H-8 is a tree on seven vertices. Every neighborhood in an H-free graph is therefore T_7-free and hence 5-degenerate (minimum degree6 embeds any seven-vertex tree greedily). In particular e(G[N(v)])<=5d(v).

LOCAL LEMMA: Suppose n>=10000, e(G)>=f(n), and delta(G)>=n/2-10.
For v with a=d(v), summing degrees of its neighbors gives
2e(N(v))>=a(delta(G)-n+a).
Together with e(N(v))<=5a this yields a<=n-delta+10<=n/2+20.
For A=N(v), B=V\A we have e(A,B)>=a(delta-10)>=a(n/2-20)>=n^2/4-15n.
Therefore a maximum cut A,B has e(A,B)>=n^2/4-15n, ||A|-n/2|<=sqrt(15n)<4sqrt(n), and at most15n missing cross edges.
If v has t internal neighbors, maximality of the cut gives at least t opposite-part neighbors. The cross edges among these two sets are edges of N(v), so t^2-15n<=e(N(v))<=5n. Thus t<5sqrt(n).
Every vertex consequently misses at most10+9sqrt(n) cross neighbors. Any four fixed vertices in one part have at least
n/2-40sqrt(n)-40>=960
common neighbors in the other part. (Write sqrt(n)=100+y, y>=0: the expression equals y^2/2+60y+960.)

The four explicit defect partitions show H embeds in (i) one internal claw plus an independent opposite part, (ii) one internal P4, (iii) one internal triangle plus an isolated vertex. The common-neighbor bound therefore forces each internal graph to have maximum degree2, no P4, and no triangle. Its components are P3,K2,K1.
Now each part has size between n/2-12 and n/2+12, and each vertex misses at most24 cross neighbors.
Since f(n)>=t_2(n)+n/3-1, at least one part A has >=n/6-1/2 internal edges. If B has an internal edge xy, exclude from A the at most48 vertices nonadjacent to x or y. At most96 internal A edges meet them. Thus choose an A edge uv adjacent to both x,y. Map H labels 7,8 to u,v and 0,4 to x,y. Choose label3 as a fresh A vertex adjacent to y, then labels1,2,5 as three fresh common B neighbors of the three chosen A vertices. Such vertices exist because cross deficits are at most24. This realizes all H edges, a contradiction. Thus B is independent.
Hence e(G)<=|A||B|+floor(2|A|/3)<=f(n), proving the local lemma.

GLOBAL: Directly t_2(n)+n/3-1<=f(n)<=t_2(n)+n/3+1. Therefore f(m)-f(m-1)>m/2-3.
Suppose n>=10^8 and an H-free G has e(G)>f(n). While order m>=10000, delete a vertex of degree<m/2-10 whenever possible. The positive integer defect e-f(m) increases by >7 at each deletion. The process cannot stop at order>=10000, by the local lemma. If it reaches order9999, its defect exceeds7(n-9999)>binom(9999,2), impossible. Therefore ex(n,H)<=f(n).
The reverse bound follows by taking K_{a,n-a} and inserting P3 components plus at most one K2 in the first part; these graphs are H-free by the direct two-case proof in agent2_counterexample_proof.md.

For n>=10^8+1 every extremal graph has minimum degree >=f(n)-f(n-1)>n/2-3, so the local classification applies. Equality requires a complete cross graph and maximum P3/K2 packing in the active part. At n=6k, f(n)=9k^2+2k, uniquely optimized at a=3k, and equality forces exactly k copies of P3 there. This yields the unique edge extremizer used in the exact cycle comparison.
