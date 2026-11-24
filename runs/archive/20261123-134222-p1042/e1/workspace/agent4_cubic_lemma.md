# Cubic local-test lemma (agent 4)
For n>=7, let M_k be the rational vector space on k-subsets of [n], identified with squarefree commutative monomials e_S. Let W:M_4->M_2 send e_T to the sum of its 2-subsets. Then ker W is spanned by the vectors
  e_c (e_a-e_b)(e_d-e_e)(e_f-e_g),
where the seven displayed labels are distinct.

Proof. Let U(e_S)=sum_{i notin S}e_{S+i} and D(e_S)=sum_{i in S}e_{S-i}. They are adjoint and DU-UD=(n-2k)I on M_k. In particular U:M_{j-1}->M_j is injective when j<=n/2, since
 ||Uv||^2=||Dv||^2+(n-2j+2)||v||^2.
Thus H_j=ker(D:M_j->M_{j-1}) has dimension C(n,j)-C(n,j-1). Its basis can be taken to be pair polytabloids p_A=product_{i=1}^j(e_{a_i}-e_{b_i}), one for each ballot set A={a_1<...<a_j}, a_i>=2i, where the distinct b_i<a_i are chosen outside A (greedy choice is possible). Each p_A is harmonic, and its leading monomial in colex order is e_A, making them independent. Their number is the required dimension.

For n>=8, repeated orthogonal splitting M_k=H_k plus U M_{k-1} gives M_4=direct_sum_{j=0}^4 U^{4-j}H_j. These are direct (and the same conclusion for n=7 holds with j<=3). One may verify this also from
 D U^r h = r(n-2j-r+1) U^{r-1}h, h in H_j,
which ensures every required map along each string is injective. Since W=D^2/2, its kernel is U H_3 plus H_4 (H_4 omitted at n=7).

For a three-pair polytabloid p, U p=sum_{c outside its six labels}e_c p: contributions using paired labels cancel because (e_a+e_b)(e_a-e_b)=0 in the squarefree algebra. Every four-pair polytabloid is (e_c-e_d)p for a three-pair p. Hence all the asserted harmonic pieces are spanned by seven-label cubic vectors.

## Application to the anchor relation lattice
Suppose I_n subset M_4(Z) is the actual anchor connecting-image lattice and costar localization to a fixed seven-label subset J maps I_n into I_7. Suppose checked I_7 equals the pair+singleton incidence lattice L_7. Every seven-label cubic functional annihilates I_7, since third differences annihilate functions of subsets of cardinality<=2. Thus each corresponding functional annihilates I_n. The lemma gives I_n tensor Q subset (ker W)^perp=im W^t, so rank I_n<=C(n,2). The n=6 bound is automatic.
