# Audit: normal AW* versus monotone completion

This note does NOT claim normal AW* implies monotone completeness.
No verified theorem or counterexample settling that implication was
identified offline. The following exact lemmas delimit the proposed route.

## 1. Positive congruence preserves existing projection suprema
If p=sup p_i in M_sa and x>=0, then x p x=sup x p_i x.
For invertible x this is an order isomorphism. For general x use x+delta,
whose products differ uniformly from those for x by O(delta), and pass to
the norm-closed positive cone.

## 2. Normality gives the correct ambient supremum for commuting positives
Let a_i increase in one masa, with supremum a there. Suppose b>=a_i.
For delta>0 set p_delta=1_[delta,infinity)(a). In the p_delta corner,
a is invertible; set c_i=p_delta a_i a^{-1} p_delta. For epsilon>0 the
high spectral projections r_i=1_[1-epsilon,1](c_i) increase to p_delta.
We have b>=a_i>=(1-epsilon)a^{1/2}r_i a^{1/2}. Projection normality
and Lemma 1 imply b>=(1-epsilon)a p_delta. Let epsilon go to zero,
then delta go to zero in norm, obtaining b>=a. This only treats a
commuting family, and does not construct a supremum for noncommuting a_i.

## 3. No proper positive-order-dense monotone-complete extension of an AW*
Let M be AW* and B a monotone-complete C* algebra containing M as a
unital C* subalgebra. Assume every nonzero b in B_+ dominates a nonzero
member of M_+. Then B=M.

First, old positive carriers are preserved. For a in M_+, let
p=supp_M(a), q=supp_B(a); q<=p. If p-q is nonzero, order density gives
0!=c in M_+ with c<=p-q. Then ac=0, so the AW right-annihilator property
implies c=(1-p)c. But c<=p implies c=pc, a contradiction. Hence p=q.

Every nonzero projection of B now dominates a nonzero projection of M:
choose old positive c below it and take c's (preserved) carrier.
For q in Proj(B), put p=sup_M{r in Proj(M):r<=q}. To see p<=q without
assuming join preservation, first let s=sup_B of this family, so s<=p.
If p-s were nonzero, projection order density would give old r<=p-s;
then p-r is an old upper bound of the family smaller than p. Thus s=p,
and p<=q. If q-p were nonzero, old r<=q-p contradicts the definition
of p. Consequently every projection of B lies in M. Spectral finite-step
approximation in the monotone-complete algebra B and norm-closedness of
M imply B=M.

Thus a putative 'regular monotone completion' that is positive-order-dense
would already prove the desired completeness (indeed for all AW* algebras).
One must not assume this density from injective-envelope essentiality:
operator-system essentiality is not positive order density. Normality of
the original AW* alone has not been shown here to supply such an extension.

## 4. Stable-normality/Naimark route remains conditional
An infinite AW* amplification preserving M as a finite corner, together
with projection normality in that amplification, would let a Naimark
dilation turn a bounded increasing positive sequence into increasing
projections and recover its supremum by corner compression. The missing
step is stable normality (and a legitimate corner-preserving amplification),
not finite-corner normality. For p_n increasing to p, finite e<=p need
not satisfy e meet p_n increasing to e; this fails even for rank-one e
and finite-coordinate p_n in B(l2). Therefore finite continuous dimension
cannot justify the required compression convergence e p_n e by this meet
argument.
