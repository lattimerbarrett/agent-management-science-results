# Links and cone transfer for lower bounds

**Lemma 1.** Every link of a pure k-decomposable complex is k-decomposable.

Induct on the number of faces. A simplex has simplex links. Otherwise choose a shedding face sigma, writing D=del_sigma Delta and L=lk_sigma Delta. Fix tau in Delta.

If sigma is contained in tau, then lk_tau Delta = lk_(tau\sigma) L, so use induction on L. Otherwise tau is in D. If sigma union tau is not a face, then lk_tau Delta=lk_tau D and induction applies. In the remaining case rho=sigma\tau is a nonempty face of lk_tau Delta with size at most k+1, and

    del_rho(lk_tau Delta) = lk_tau D,
    lk_rho(lk_tau Delta) = lk_(tau\sigma) L.

The first complex is pure of the same dimension as lk_tau Delta because D and Delta are pure of the same dimension. Both right-hand complexes are k-decomposable by induction. Thus rho is a valid shedding face.

**Lemma 2.** Joining a k-decomposable complex with a simplex preserves k-decomposability.

Induct through the decomposition, using the same shedding face sigma: deletion and link commute with joining a disjoint simplex. Simplices join to simplices.

**Proposition.** For every s>=0, b(d+s,k)>=b(d,k).

Suppose a pure d-dimensional k-decomposable Delta on V cannot complete using r fresh vertices. Let B be a fresh s-element set and form Delta*2^B, a pure (d+s)-dimensional k-decomposable complex. If it had a completion using r fresh vertices A, take lk_B throughout that completion. Lemma 1 keeps every resulting link k-decomposable. A new facet changes this link exactly when it contains B; those facets correspond bijectively to all missing (d+1)-subsets on V union A. The extracted subsequence is therefore a forbidden completion of Delta using r fresh vertices. This proves obstruction transfer, and hence the claimed inequality.

This transfer does not increase the number of required fresh vertices. In particular, it does NOT establish the sharp lower bound asked in the problem.
