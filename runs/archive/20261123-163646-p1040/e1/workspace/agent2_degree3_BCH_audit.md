# Independent audit of the class-three integral coordinates

Let x_i=exp(e_i), and use ordinary free-group Magnus variables X_i=x_i-1.
For a relator r in gamma_2 of the free group on the Magnus generators,
write its truncated Magnus expansion 1+r_2(X)+r_3(X).
Substituting X_i=e_i+e_i^2/2+e_i^3/6 gives

  log(r)_2 = r_2(e),
  2 log(r)_3 = 2 r_3(e) + sum_(i,j) c_ij(e_i^2 e_j+e_i e_j^2),

where r_2=sum c_ij X_i X_j. This is precisely `initial_vector` in
`agent1_degree3_closure.py`. The Lyndon coefficient functions verify
that both displayed homogeneous components lie in the integral free Lie
lattice after the indicated doubling.

For an IA-generator word w with Magnus expansion 1+f_1+f_2+..., write
l=f_1(e) and q=2 f_2(e)-l^2+sum_i coeff_(X_i)(f_1)e_i^2. Then
log(w)=l+q/2+terms of degree>=3. Therefore an endomorphism sending
x_i to w_i acts on the displayed coordinates by

 [e_i,e_j] -> [l_i,l_j] in degree2,
             [q_i,l_j]+[l_i,q_j] in doubled degree3;
 2r_3      -> (2r_3)(l_1,...,l_m).

This exactly matches `action_matrix`. Normal conjugation by x_i adds
2[e_i,r_2] to the doubled cubic coordinate, matching the closure step.
All relators considered lie in gamma_2, whose elements commute modulo
gamma_4; hence the logarithms of their products are additive through
degree3. Integral kernel combinations of quadratic coordinates therefore
produce the exact cubic relations contributed by these true relators.
When quadratic coordinates vanish, the doubled cubic row is even, and
division by2 recovers the honest integral degree-three free Lie element.

No spurious factors2 or3 were found in this computation. The observed
Smith deficit (Z/2)^5 directsum (Z/6)^9 is a property of the current
true-relator cover, not a proof about IA itself.

Genuine added relator families and exact reproducible provenance:
- `agent2_peiffer_degree3.py`: 81 Peiffer-action identities;
- `agent2_aut_consistency_degree3.py`: 135 Aut-action-loop identities;
- `agent2_tail_relators.py`: 75 conjugated-tail/partial-inner identities.
All true action words are checked by reduced free-group substitution.
The combined computation `agent2_degree3_tailcombined.py` reproduces
rank197 and the stated deficit; it explicitly prints INCOMPLETE.
