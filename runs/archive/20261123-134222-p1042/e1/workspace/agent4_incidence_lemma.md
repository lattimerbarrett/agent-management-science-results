# Incidence presentation lemma (agent 4)
Let n>=6, let M_k be free on the k-subsets of [n], and set r_A=sum_{T containing A, |T|=4} [T]. Then
M_4 / <r_A: |A|=1 or 2> = Z^{C(n,4)-C(n,2)} plus Z/2.

Here is a self-contained simultaneous integral diagonalization. Call A={a_1<...<a_j} ballot when a_i>=2i. The vectors b_A^k=sum_{T containing A,|T|=k}[T], for ballot A with |A|<=min(k,n-k), form a Z-basis of M_k.
For k<=n/2, prove this by induction on n, splitting k-subsets into those omitting and containing n. The ballot indices not containing n index the basis for M_k([n-1]); those containing n, after removing n, index the basis for M_{k-1}([n-1]). At n=2k the first family has rank bound k-1 automatically. This gives block triangular matrices with unimodular diagonal blocks.
For k>n/2, take complements and put q=n-k. Complement carries b_A^k to sum_{B subset A}(-1)^|B| b_B^q. Every subset of a ballot set is ballot; this is triangular with diagonal +/-1. Thus the basis assertion holds in all cases.

Let I_{s,4}:M_s->M_4 carry [S] to r_S. Then direct counting gives
I_{s,4}(b_A^s)=C(4-|A|,s-|A|) b_A^4.
For s=1,2 all ballot A in the domain occur in the target because n>=6. Thus the sum of the two image lattices is diagonal in the target ballot basis: coefficient gcd(4,6)=2 at A=empty; gcd(1,3)=1 at |A|=1; coefficient1 at |A|=2; coefficient0 for larger A. The number of target basis vectors of rank<=2 is C(n,2), proving the formula.

The ballot count at rank j is C(n,j)-C(n,j-1), by the standard reflection bijection from nonballot j-subsets to (j-1)-subsets. This count is also implicit in the unimodular basis proof.
