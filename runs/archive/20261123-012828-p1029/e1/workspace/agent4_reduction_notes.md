# Verified reductions and local lemmas (agent 4)

## 1. Tracial case
If tau is a normalized trace, then for every N,
N eta = sum_{n<N} tau(a_{n+1}-a_n) = tau(a_N-a_0) <= 1.
Choosing N > 1/eta is a contradiction. In a matrix factor M_d(C), a normalized quasitrace is a trace: unitary invariance makes its value on every rank-one projection 1/d, and abelian spectral decomposition then gives tau(h)=Tr(h)/d for self-adjoint h. The complex decomposition gives the identity on all elements.

## 2. Constant-gap interpolation preserves all upper bounds
Assume q is normalized, positively homogeneous, and order preserving on positive elements. Let 0<=s_n<=s_{n+1}<=1. Suppose there is epsilon>0 such that every tail contains indices j<k with q(s_k-s_j)>=epsilon. Fix 0<eta<min(epsilon,1). Construct a_n and increasing k_n recursively, maintaining a_n<=s_{k_{n-1}}. Given a_n, tail non-Cauchyness and monotonicity supply k_n>k_{n-1} with g_n=q(s_{k_n}-a_n)>=epsilon. Put
  t_n=eta/g_n,  a_{n+1}=(1-t_n)a_n+t_n s_{k_n}.
Then eta<=t_n<=1, a_n<=a_{n+1}<=s_{k_n}, and q(a_{n+1}-a_n)=eta.

Every common upper bound of the s_n bounds the a_n. Conversely, let y bound every a_n and fix j. Once k_n>=j, the recursion gives
  a_{n+r} >= P_{n,r} a_n+(1-P_{n,r})s_j,
where P_{n,r}=product_{l=n}^{n+r-1}(1-t_l) <=(1-eta)^r. The lower bound converges in norm to s_j. Since y bounds a_{n+r}, norm-closedness of the positive cone gives y>=s_j. Hence the two sequences have identical upper-bound sets, and either both or neither has a least upper bound.

This is a reduction only: it does not exclude non-Cauchy monotone sequences.

## 3. Weighted finite-join lemma
Let p_1,...,p_m be projections in a finite AW* factor and let t_j>0, R>0 satisfy sum_j t_j p_j<=R1. Let P=diag(p_j), V=[sqrt(t_1)p_1 ... sqrt(t_m)p_m], G=V*V, and delta_j=1-t_j/R. Assume D=sum_j delta_j<1. (Nonzero p_j force t_j<=R.) Then 0<=G<=RP. The positive block matrix B=P-G/R has diagonal blocks delta_j p_j. A positive block matrix has norm at most the sum of its diagonal-block norms, so ||B||<=D. Thus G>=R(1-D)P. Consequently V has closed range and its polar partial isometry has initial P and final r=join_j p_j. Therefore d(r)=sum_j d(p_j), and
  r <= (sum_j t_j p_j)/(R(1-D)).
The operator-norm estimate follows from block Cauchy-Schwarz: if B=S*S and xi=(xi_j), then
 ||S xi|| <= sum_j ||S_j xi_j|| <= (sum_j ||B_jj||)^(1/2)||xi||.
This argument can be read in any faithful Hilbert-space representation.

For equal weights t_j=1 and R=C, D=m(1-1/C), so when m-(m-1)C>0 the join of m projections has dimension m d and a disjoint-block family of such joins has Bessel bound C/[m-(m-1)C]. The scalar candidate d(C)=1-1/C exactly saturates this recurrence; it does not prove exhaustion.

## 4. Status
The needed diffuse-factor step has NOT been proved. In particular none of the following has been established here:
- bounded positive partial sums imply q(b_n)->0;
- faithful quasitraces are strictly or uniformly order monotone;
- normality of finite AW* projection joins implies monotone sequential completeness;
- the commutator ideal of an arbitrary hyponormal-generated C*-algebra is stable.
These must not be used as theorems without a separate proof or a verified reference.
