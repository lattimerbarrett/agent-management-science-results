from pathlib import Path
Path('workspace/agent4_elementary_highmindeg.md').write_text(r'''# Completely elementary high-minimum-degree proof for the diagnostic H

No stability theorem is needed. Let C=10, N=100^8=10^16. Let G be H-free of order n>=N, e>=f(n), delta>=n/2-10.

1. Since H-8 is bipartite on 7 vertices with colorclass sizes 3 and 4, H is a subgraph of K1 join K4,4. Hence EVERY G[N(v)] is K4,4-free.

2. An arbitrary K4,4-free graph J on at most n vertices has e(J)<=3n^(7/4). Indeed, count pairs consisting of a 4-set and a common neighbor:
 sum_v binom(d(v),4)<=3 binom(n,4).
Using binom(d,4)>=(d-3)_+^4/24 and convexity gives average degree <=3+3^(1/4)n^(3/4), and thus e(J)<=3n^(7/4).

3. Consequently the number t of triangles in G is at most n^(11/4). The elementary identity/inequality
 3t>=sum_v d(v)^2-ne>=4e^2/n-ne
implies e<=n^2/4+3n^(7/4): put e=n^2/4+x>n^2/4, then nx+4x^2/n<=3t<=3n^(11/4).

4. Choose v with degree at most the average n/2+6n^(3/4). Its neighborhood A has size a between n/2-10 and n/2+6n^(3/4). With B its complement,
 e(A,B)=sum_{u in A}d(u)-2e(A)
 >=a(n/2-10)-6n^(7/4)
 >=n^2/4-10n-6n^(7/4).
A maximum-cross cut therefore also has at least this many cross edges. Relabel it A,B. The number D of missing cross edges is at most 16n^(7/4), and |a-n/2|<=4n^(7/8).

5. If any vertex has at least 5n^(7/8) neighbors in EACH part, the cross graph between these neighborhood sets has at least
 25n^(7/4)-D>=9n^(7/4)
edges. It is contained in G[N(v)], contradicting step 2. In a maximum-cross cut internal degree is at most cross degree; hence every internal degree is less than 5n^(7/8). The minimum-degree bound then implies that each vertex misses at most 10+9n^(7/8) cross edges.

6. Any four same-part vertices have a common opposite-part neighborhood of size at least
 n/2-40n^(7/8)-40>=n/10-40>8,
where n>=100^8 was used. The explicit claw, P4 and triangle-plus-isolate patterns of H therefore show that neither internal graph contains a claw, P4, or triangle. (For the triangle choose any fourth distinct same-part vertex first.) Thus all internal components are P3, P2, or isolates.

7. Internal maximum degree<=2 and delta>=n/2-10 now imply |a-n/2|<=12 and every vertex has at most K=24 missing cross neighbors. Since e>=f(n)>=t2(n)+n/3-1, at least one part, say A, has >=n/6-1 internal edges.

8. If B has an edge pq, delete from A all vertices not adjacent to both p and q. At most 2K vertices, hence 4K internal edges, are lost; plenty remain. Choose an A-edge uv with both endpoints adjacent to p,q, map H7=u,H8=v,H0=p,H4=q. Choose H3=w in A adjacent to q and distinct from u,v. Finally choose H1,H2,H5 distinct in the common B-neighborhood of u,v,w, excluding p,q. Every one of the twelve H edges is present. Contradiction. Thus B is independent.

9. It follows e<=ab+floor(2a/3)<=f(n). If equality and n divisible 6, the objective is uniquely maximized by a=n/2 and the internal graph is a P3-factor, with no missing cross edges.

10. The progressive-deletion argument now has explicit thresholds. The bounds
 t2(m)+m/3-1<=f(m)<=t2(m)+m/3+1
imply f(m)-f(m-1)>m/2-3. Deleting a vertex of degree<m/2-10 strictly increases e-f by more than 7. Starting from a counterexample of order n>=N^2=10^32, one cannot stop above N by steps 1--9; reaching N would give defect >7(n-N), larger than binom(N,2). Thus ex(n,H)<=f(n) for all n>=10^32. The P3-packing construction attains f, proving equality. For n>=10^32+1, every extremal graph has minimum degree >=f(n)-f(n-1)>n/2-3, so steps 1--9 classify it.

This removes the ONLY deep external theorem from the counterexample argument. Constants are deliberately very coarse but explicit and valid.
''')
print('wrote elementary proof')
