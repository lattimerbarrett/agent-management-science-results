# Dual characteristic and norm lemma (complete)

Let p>1, q=p/(p-1), A=W^(1/p), and V=W^(-1/(p-1)).
For a fixed interval I normalize Lebesgue measure to probability. Put
F=(E_x (E_y ||A(x)A(y)^(-1)||^q)^(p/q))^(1/p).
Define G by replacing A by A^(-1) and p by q. Then

    F/32 <= G <= 32 F.

Consequently [V]_{A_q}^{1/q} is within a factor 32 of
[W]_{A_p}^{1/p}. Constants are deliberately nonoptimal.

Proof. Finite F and a suitable fixed x imply E||A^(-1)||^q<infinity;
E||A||^p<infinity follows from local integrability of W. Thus
n_+(v)=(E|Av|^p)^(1/p), n_-(v)=(E|A^(-1)v|^q)^(1/q)
are genuine finite-dimensional complex norms.
For any complex norm n on C^2, choose a pair u_1,u_2 in its closed
unit ball maximizing |det(u_1,u_2)|. The maximum exists, is positive,
and both vectors have norm one. If v=a_1u_1+a_2u_2 has n(v)<=1,
replacing u_j by v and using determinant maximality proves |a_j|<=1.
Thus for general v, max|a_j|<=n(v)<=|a_1|+|a_2|.
Let R be the positive definite matrix with |Rv|^2=|a_1|^2+|a_2|^2.
We obtain |Rv|/sqrt(2)<=n(v)<=sqrt(2)|Rv|.
Choose B,C as such reducing matrices for n_+,n_- respectively.

The following elementary observation is used twice. If
n(v)=(E|M v|^r)^(1/r) is reduced by R as above, and T is fixed, then

  (1/2)||RT|| <= (E||MT||^r)^(1/r) <= 2sqrt(2)||RT||.

Indeed the middle quantity is >=max_j n(Te_j), giving the lower bound,
and is <=n(Te_1)+n(Te_2) by Minkowski, giving the upper bound.
Apply this first with M=A(y)^(-1), T=A(x), r=q, and use that
||A(x)A(y)^(-1)||=||A(y)^(-1)A(x)|| (adjoints).
The inner norm is between ||CA(x)||/2 and 2sqrt(2)||CA(x)||.
Since ||CA(x)||=||A(x)C||, apply the observation a second time with
M=A(x), T=C, r=p. It follows that

  ||BC||/4 <= F <= 8||BC||.

For G exchange A with A^(-1), B with C, and p with q; obtain
||CB||/4 <= G <= 8||CB||. Since B,C are Hermitian,
||BC||=||(BC)^*||=||CB||. This proves the claimed factor 32.
Taking suprema over intervals proves the characteristic statement.

The Banach dual of L^p(W), under the unweighted integral pairing, is
L^q(V): this follows isometrically by conjugation with A, because
V^(1/q)=A^(-1). Smooth compactly supported functions are dense (truncate,
then use regularity of the finite measures defined by the locally
integrable matrix entries). H is skew-adjoint on smooth test functions.
Therefore its bounded extension on the two dual weighted spaces has
the same operator norm. Combining this with characteristic comparability
in both directions gives the exact relation between optimal powers:

    beta(q)=(p-1) beta(p).

This duality statement does not determine beta(p) from beta(2).
