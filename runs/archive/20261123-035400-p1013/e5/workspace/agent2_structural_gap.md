# Structural gap supplement

Assume H has chi(H)=r+1 and embeds in both a fixed complete r-partite graph plus an internal star and a fixed complete r-partite graph plus an internal matching. The high-minimum-degree structural lemma (agent3_structural_lemmas.md) therefore gives fixed epsilon>0, M such that every sufficiently large H-free F with delta(F)>=(p-epsilon)|F| has e(F)<=t_r(|F|)+M, p=(r-1)/r. This conclusion uses only those two templates and ordinary Erdos-Simonovits stability.

Claim: ex(n,H)<=t_r(n)+M for all sufficiently large n, without any preliminary linear-excess bound.

Proof. Let G edge-extremal on n vertices; e(G)>=t_r(n). Repeatedly delete a vertex of degree below (p-epsilon)m, where m is the current order. Write D_m=t_r(m)-e(G_m). One deletion gives
 D_(m-1)=D_m+d(v)-[t_r(m)-t_r(m-1)]<=D_m-epsilon*m+1,
because t_r(m)-t_r(m-1)=m-ceil(m/r)>=pm-1. Initially D_n<=0.

The process stops after o(n) deletions. Indeed, if for any fixed c in (0,1) it made cn deletions, then at m=(1-c)n+O(1), summation gives D_m<=-epsilon*(c-c^2/2)n^2+O(n). But Erdos-Stone gives D_m>=-o(m^2), contradiction. Thus the first high-minimum-degree core has order m=n-k with k=o(n). Its deficit is at least -M by the structural lemma, whereas summing the deletion inequalities gives D_m<=-k[epsilon*(n-k)-1]. For n large this is incompatible with k>=1. Hence k=0 and e(G)<=t_r(n)+M.

Corollary (uniform linear gap). If ex(n,H)<=t_r(n)+a*n+C eventually for any a<1/(2r), then H embeds into a fixed complete r-partite graph plus an internal matching, since that insertion adds floor(floor(n/r)/2)=n/(2r)+O(1) edges. It likewise embeds into a fixed complete r-partite graph plus an internal star, since that adds n/r+O(1) edges. Therefore the claim applies: ex(n,H)=t_r(n)+O_H(1).

This is an additional consistency check, not the requested construction. Combined with the team's r>=3 cycle obstruction it excludes the entire interval [0,1/(2r)) from S_r; the boundary 1/(2r) and full correct set are not determined here.
