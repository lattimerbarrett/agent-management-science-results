# Two integral degree-two relations

Write a_i;jk=e_i^* tensor [X_j,X_k] for the signed degree-one Magnus basis.

## Same target

Fix i and put K=<x_j:j!=i>. Define T_u(x_i)=x_i u, fixing K, and P_v(x_i)=x_i, P_v(y)=v y v^{-1} for y in K. Both T:K->Aut(F_n) and P:K->IA_n are homomorphisms. Moreover P_v T_u P_v^{-1}=T_{vuv^{-1}}, so [P_v,T_u]=T_[v,u]=[T_v,T_u]. If u,v in gamma_2(K), then T_u,T_v are in IA and P_v in gamma_2(IA). Therefore [T_v,T_u] lies in gamma_3(IA). This proves every same-target wedge a_i;jk wedge a_i;qr is zero in gr_2(IA), with no restrictions on overlap among j,k,q,r beyond avoidance of i. The exact automorphism identity was checked for all basic commutator tails through n=6 in same_target_relation.py; its displayed algebraic proof is valid for all n.

## Dummy contraction index

Take five distinct i,p,k,q,r. The wedge R=a_i;pk wedge a_q;qr is induced by two exactly commuting Magnus automorphisms. Apply an elementary Nielsen automorphism whose homology action is e_p->e_p+e_q. Its action on the two factors is a_i;pk->a_i;pk+a_i;qk and a_q;qr->a_q;qr-a_p;qr. Subtract R and the also-exact commuting wedge a_i;qk wedge a_p;qr. Since every GL_n(Z) conjugate of a true gr_2 relation is again a true relation, the expansion gives

a_i;pk wedge a_p;qr = a_i;qk wedge a_q;qr in gr_2(IA).

Thus a nonzero derivation bracket column with union support five (exactly one contraction) may be replaced integrally by one supported on four labels. This does NOT by itself prove the whole all-rank kernel is generated in support four: relations between support-four columns can involve more labels.
