# Robust finite two-amplitude game
Let V be finite-dimensional, l_0,l_1 independent covectors, F_0,F_1 vectors,
c_ij=l_i F_j, with c_00,c_11<0. Set R_j=I-2F_j l_j/c_jj.
A firing of j is legal if l_j(w)>0. Suppose firings alternate 0,1,0,1,... .
If either offdiagonal c_01,c_10 is nonpositive, there cannot be three legal alternating firings starting with the opposite endpoint: after a positive firing flips its own growth negative, firing the other one cannot make it positive again when the relevant cross coefficient is nonpositive. Thus any infinite alternating chain requires both offdiagonals positive.
Assume c_01,c_10>0 and k=c_01*c_10/(c_00*c_11)<1. After positive diagonal rescaling of the growth coordinates, the normalized firing matrices are
 S0=[[-1,0],[2b,1]], S1=[[1,2a],[0,-1]], a,b>0, ab=k.
For one full cycle S1*S0, trace=4k-2 and determinant=1. If u_n denotes the amplitude just before the nth firing of endpoint0, then
 u_(n+2)=(4k-2)u_(n+1)-u_n.
Writing theta=arccos(2k-1) in (0,pi), every nonzero solution is
 u_n=A*cos(n theta)+B*sin(n theta).
No such sequence can remain nonnegative for more than floor(pi/theta)+3 consecutive indices: its phase advances by theta<pi, so cannot jump across the entire negative semicircle. Hence every exact legal alternating chain is finite, with a bound depending only on k.

## Robustness
Choose an integer N larger than that bound. For every nonzero growth vector x, among the first N firing tests of the exact alternating game one is strictly negative. By compactness of the growth unit sphere, some such test is <=-c|x|, for a uniform c>0. Thus the conclusion remains true for perturbed firing maps
 w_(j+1)=R_(j mod2) w_j+e_j,
provided |e_j|<=epsilon_j |w_j|, epsilon_j->0, and each sufficiently late block of N tests starts with a nongrazing state
 |(l0(w_j),l1(w_j))|>=c0 |w_j|,
with c0>0 fixed. Indeed finite products of the two fixed Rj bound all |w_(j+m)| by C_N|w_j| for m<=N; the accumulated errors in the N tests are o(|w_j|)=o(|growth_j|), contradicting the fixed negative margin.

This lemma is conditional on the exact restarted-CG orbit admitting the stated pulse/flight asymptotics and nongrazing estimate. It does not itself prove these hypotheses or k<1.

## Nongrazing for the cooperative s=3 nearest-wall pair
Assume the hard-case orientation c<a<b, left negative mode mu<a, right negative mode nu>b, and choose the fixed velocity covector cvel so theta velocity has the sign of cvel(w) inside the edge. Let A be the norm-variation covector at the left wall. The exact raw endpoint identity is
 A=alpha0*cvel+beta*L_mu(a)+gamma*L_nu(a),
with beta>0,gamma<0. Let T be intrinsic left-to-right flight transport. Then
 l0=L_mu(a), l1=L_nu(b)*T,
 F0=F_mu(a), F1=T^-1*F_nu(b).

**Rank-one row transport.** Since theta velocity is scalar(theta)*cvel, for w in ker(cvel) the polynomial q=gw+f*DG_theta(w)-A_theta(w) vanishes at the five base nodes. Thus q=P5*C_theta(w). Differentiation in theta gives
 f*(DG_theta(w))'=A_theta'(w)+P5*C_theta'(w).
The residues of P5 modulo f are not constant: otherwise P5Q=-L modulo f and nonconstant linear Q would give a degree-one polynomial equal to zero modulo the cubic f, impossible since L>0. Therefore divisibility by f forces C_theta'(w)=A_theta'(w)=0, and then DG_theta(w)'=0. It follows that each L_z(theta)-L_z(a) annihilates ker(cvel), so is a scalar multiple of cvel.
The flight transport T=I+r*cvel has the same property. Hence l1-L_nu(a) is a multiple of cvel, and
 A=alpha*cvel+beta*l0+gamma*l1
with the SAME beta>0,gamma<0.

If the pair is cooperative, C00=l0(F0)<0 and C10=l1(F0)>0. Left-mode repulsion gives cvel(F0)>0. The exact gain identity gives A(F0)=4(L+f(mu)^2)>0. Applying the last displayed identity to F0 shows
 alpha*cvel(F0)=A(F0)-beta*C00-gamma*C10>0,
hence alpha>0.
At any outgoing left-wall state, cvel(w)>=0. If physically A(w)<0, then
 -A(w)<= (beta+abs(gamma))*max(abs(l0(w)),abs(l1(w))).
The polynomial-total-variation cone ||w||<=C*(-A(w)) therefore yields the uniform nongrazing estimate required by the robust game lemma.

Thus the nongrazing issue for a genuinely cooperative nearest-pair pulse chain reduces only to the established endpoint identity, norm gain, repulsion sign, and TV cone; no new transported-kernel inequality is required. This still does NOT establish that every recurrent boundary trajectory reduces to such a pure two-charge chain, nor prove cooperative k<1.

Positive scalar renormalizations between firings do not change the lemma: for w_(j+1)=sigma_j*(R_j w_j+e_j), sigma_j>0, divide w_j by the product sigma_0...sigma_(j-1). The transformed error remains o(the transformed state norm), nongrazing ratios and all legality signs are unchanged. This applies directly to deficit-normalized compact blowups with A=-1.
