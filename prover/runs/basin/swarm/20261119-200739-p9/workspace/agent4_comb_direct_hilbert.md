# Direct Hilbert-transform lower bound for the inner-quarter comb

Fix p>2, v=1/(p-1), la=Q^(-1), lc=Q^(-v), ra=2-la,
rc=2-lc, and k=Q^(v/p). Assume Q large enough that rc>=3/2.
At an active interval I with state(a,c,h), split into four equal
quarters, in increasing spatial order:

  B+ : (la a,lc c,h+k/c), terminal;
  G+ : (ra a,rc c,h+k/c), continue;
  G- : (ra a,rc c,h-k/c), continue;
  B- : (la a,lc c,h-k/c), terminal.

Start on[0,1] at(1,1,0), and terminate all remaining active intervals
after L cycles without changing their current state. Write a_L,c_L,h_L
for the resulting step functions, and

 M_L=[[a_L^(1/p),a_L^(1/p)h_L],[0,a_L^(1/p)/c_L]].

The actual matrix weight is W_L=(M_L* M_L)^(p/2), so its root is
|M_L|. Polar decomposition shows that its norm and characteristic are
exactly the ones computed with M_L. The independent moment/characteristic
proof is in agent2_comb_characteristic.md; below only the direct H
lower bound is proved.

Define compactly supported tests
f_L=c_L(-h_L,1), g_L=a_L(1,h_L) on[0,1], zero outside. Each cycle
preserves averages of a,c,ah,ch (check the two rotation children,
then the two stretching children). In particular int a_L=int c_L=1,
and

 |M_L f_L|^p=a_L,  |M_L^(-*)g_L|^q=a_L.

Both test norms are exactly1. Let

 B_L=(1/pi) integral_[0,1]^2 a_L(x)c_L(y)
               (h_L(x)-h_L(y))/(x-y) dxdy.

For finite L this is the ordinary Hilbert pairing <Hf_L,g_L>:
within each terminal cell the numerator is zero, and across distinct
cells the kernel is integrable, including adjacent-cell corner
singularities. Let C_L be the part of B_L with x,y in DIFFERENT
TOP-LEVEL quarters. B_0=0. On each of the two active quarters,
a,c,h,space transform as

 a=ra a_copy, c=rc c_copy,
 h=+/-k+(1/rc)h_copy, x=offset+x_copy/4.

Consequently its internal contribution to B_L is (ra/4)B_(L-1).
The two bad quarters are constant and have zero internal contribution.
Thus EXACTLY

                  B_L=C_L+(ra/2)B_(L-1).                 (1)

We prove that C_L has a limit C_infinity and, as Q tends to infinity,

       C_infinity/k tends to a strictly negative constant <=-2/pi. (2)

This will imply B_L tends to C_infinity/(1-ra/2)=2Q C_infinity,
and hence some finite L=L(Q) satisfies |B_L|>=c Q k.

## Probability/coupling description

mu_a,L=a_L dx and mu_c,L=c_L dx are probability measures. Under
mu_a, the number N of successful cycles before absorption has law

 P(N=n)=(la/2)(ra/2)^n,

truncated at L, where the residual survival mass is(ra/2)^L. Under
mu_c replace a by c. Conditional on survival/exitage, the signs
sigma_0,sigma_1,... are independent symmetric signs. The spatial
coordinate lies in the quarter sequence G_(sigma_j) until the exit,
then is uniform in the corresponding B_(sigma_N) quarter. Also

 h_L/k=sum_(j=0)^N sigma_j rc^(-j),

with the sum stopped at L-1 for a surviving active leaf. Therefore
|h_L|<=k rc/(rc-1)<=3k.

For fixed Q, coupling the truncated and infinite exit depths shows
that the joint laws of(x,h_L/k), under each of mu_a,L and mu_c,L,
converge as L tends to infinity. As Q tends to infinity, the exit
depths under BOTH measures tend to infinity, ra,rc tend to2, and
these joint laws tend to one common law(nu,H). Here nu is the equal
probability Cantor measure for the maps

 F_+(x)=1/4+x/4,  F_-(x)=1/2+x/4,

and H=sum_(j>=0) sigma_j/2^j. Coupling with common infinite sign
sequences proves the asserted convergence directly: finite prefixes
converge and the tails are uniformly bounded geometrically.

## Uniform integrability of the cross-quarter kernel

Only adjacent top-level quarters can have x-y arbitrarily small.
At every top-quarter boundary, BOTH adjacent strips of length1/16
are already terminal bad states after at most two cycles. For L>=2,
on these strips one has a_L<=2la and c_L<=2lc. Hence, since |h_L|<=3k,
the contribution in absolute value from pairs in different top quarters
with |x-y|<1/16 is at most

 C k la lc int_0^(1/16) int_0^(1/16) 1/(u+w) dudw
 <=C' k la lc.

There are only three boundaries and two orientations. This bound is
uniform in L and tends to zero after division by k as Q tends to
infinity. On |x-y|>=1/16 the cross kernel divided by k is uniformly
bounded, and joint-law convergence applies. One may insert a continuous
cutoff vanishing at distance<=1/32 and equal to1 at distance>=1/16;
the omitted near-boundary piece satisfies the same bound. Quarter
boundaries have zero limiting nu-mass. For fixed Q the near-boundary
piece is already independent of L>=2 (the states there have stabilized),
so this argument also proves existence of C_infinity. In particular
|C_L|<=Ck uniformly in Q,L.

## Sign of the limiting cross integral

The limiting measure is supported only in the two active top quarters,
with mass1/2 on each. On the left copy, H=1+H_copy/2 lies in[0,2]
and has mean1; on the right, H=-1+H_copy/2 lies in[-2,0] and has
mean-1. Thus for a left x and right y, H(x)-H(y)>=0 whereas x-y<0.
The same negative sign holds in the opposite order. Since |x-y|<=1/2,
its reciprocal absolute value is at least2. The integral of the
nonnegative H difference on each ordered pair of quarters equals
(1/2)(1/2)(1-(-1))=1/2. Therefore the limiting cross form is at most

                -(1/pi)*2*(2*1/2)=-2/pi.

The limiting Cantor supports within these quarters are separated by
at least1/8, so there is no limiting singularity. This proves(2).

For every sufficiently large Q (depending only on p), C_infinity<=-k/pi.
Equation(1), boundedness and convergence of C_L give
B_L ->2Q C_infinity<=-2Qk/pi. Thus choose finite L with

                   |<Hf_L,g_L>|>=Qk/pi.                  (3)

Together with the characteristic upper [W_L]Ap<=C_pQ and the two
unit test norms, this yields

 ||H||Lp(W_L)>=c_p Q^(1+1/[p(p-1)]).

Every finite-L weight is bounded above and below by positive constants
(on the periodic extension or the constant bad-state outside extension),
and f_L,g_L are bounded compact step functions. Standard smooth
approximation in unweighted Lp, boundedness of the ordinary Hilbert
transform on Lp, and those finite weight bounds pass(3) to smooth
compactly supported input functions. Therefore it is valid for exactly
the input class in the question.

## Computational verification

agent4_comb_direct_hilbert_checks.py computes exact cell-integrated
Hilbert pairings for depths3,5,7,8 (up to766terminal intervals),
p=2,3,5 and Q=10,100,10000. It evaluates the cross form separately.
For p2,Q10000,depth8, C_L/k=-1.2207455384562889, agreeing with the
strict negative limit above. All pairings are evaluated from the
closed integral of1/(x-y), NOT a sampled singular kernel.
