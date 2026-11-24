# Strict-left dual-root deflation for the virtual-probe argument

This supplements `agent3_virtual_root_lemma.md`. All estimates below hold on a
sufficiently late actual orbit tail; constants may depend on the fixed probe
zeta, but not on the tail index. Write the index for consecutive restart blocks.

## 1. Exact identities and separation

Retain only the spectral nodes which never disappear; all weights p_{k,i} are
positive. Let d_i be the derivative at lambda_i of the polynomial through
these nodes, f_k the monic primal degree-s polynomial, N_k its norm, and H_k
the monic dual polynomial. Set q_{k,i}=1/(d_i^2 p_{k,i}) without normalizing.
Duality and the primal update give exactly

    H_k(lambda_i)=d_i p_{k,i} f_k(lambda_i)/N_k,
    H_{k+1}(lambda_i)/H_k(lambda_i)=f_k(lambda_i)f_{k+1}(lambda_i)/N_{k+1},
    q_{k+2}=constant*q_k*(H_k/H_{k+1})^2,
    q_{k,i}H_k(lambda_i)^2=p_{k,i}f_k(lambda_i)^2/N_k^2.          (1)

Thus sum_i q_{k,i}H_k(lambda_i)^2=1/N_k, uniformly bounded above and below.
Choose a fixed probe zeta below c, arbitrarily close to c, avoiding all spectral
nodes and limiting primal zeros. All non-strict slow dual roots are above zeta.
Every actual spectral node below zeta is a strict contractor and its primal
weight is O(rho^k), some rho<1. Each corresponding dual root a_{k,j} is simple,
is separated from all other limiting roots, and is lambda_j+O(rho^k).
These statements follow directly from (1), uniform primal Gram invertibility,
and the simple-root implicit function theorem. Uniform Gram invertibility on
the orbit closure follows from N_k>=N_0>0: a singular limiting degree-(s-1)
Gram matrix would put the limiting measure on at most s-1 nodes, making the
monic degree-s norm zero. In fact support at most s also contradicts N_0>0.

Let D_k(x)=product_j(x-a_{k,j}) over precisely these strict-left roots, and let
Hhat_k=H_k/D_k. All roots of Hhat_k are uniformly above zeta on this tail.
Hhat_k is EXACTLY the monic orthogonal polynomial for the positive measure
qhat_{k,i}=q_{k,i}D_k(lambda_i)^2: its orthogonality against x^j follows by
orthogonality of H_k against D_k x^j, whose degree is at most deg(H_k)-1.
Moreover,

    qhat_{k+2}=constant*qhat_k*(Hhat_k/Hhat_{k+1})^2*E_k,
    E_{k,i}=[D_{k+2}(lambda_i)/D_{k+1}(lambda_i)]^2.             (2)

Off the strict-left spectral nodes, E_{k,i}=1+O(rho^k). At strict-left nodes
this relative estimate is NOT asserted. Instead E_{k,i} is uniformly bounded:
use (1) to write its square root as

    D_{k+2}/D_{k+1}=(f_{k+1}f_{k+2}/N_{k+2})*(Hhat_{k+1}/Hhat_{k+2}).

The primal factor is bounded; the hatted evaluations at these left nodes are
bounded away from zero. Most importantly, the cancellation

    qhat_k Hhat_k^2=q_k H_k^2=p_k f_k^2/N_k^2                 (3)

means the strict-left part of this measure is O(rho^k), with total mass 1/N_k.
There is no reciprocal-Gram condition number hidden in these estimates.

## 2. Adding an infinitesimal primal probe

For a fixed triple k,k+1,k+2, add primal weight eta at zeta at time k. Use eta
as CURRENT probe weight, not as probe weight at the start of the infinite
orbit. The latter coefficient can grow or decay exponentially. Renormalizing
the perturbation parameter separately on each triple multiplies all three
virtual displacements by one positive number and changes neither their ratios
nor the signed root inequality.

The augmented dual polynomial tends to (x-zeta)H_j as eta decreases to zero.
Its extra root is a_j(eta)=zeta+eta alpha_j+O(eta^2). With the current-time
normalization, alpha_k=-P_n(zeta)f_k(zeta)/(N_k H_k(zeta)). It is bounded away
from zero and infinity uniformly in k. The same holds for alpha_{k+1} and
alpha_{k+2} with this common triple normalization: the probe primal weights
over this finite triple have ratios f_j(zeta)^2/N_j, bounded away from zero
and infinity. Their ratios are the ratios from the initial-weight convention
used in agent3's lemma, hence obey its exact beta formula.

Uniformly for small eta, the augmented strict-left roots stay
lambda_j+O(rho^k). Indeed the augmented primal coefficients and their eta
derivatives are uniformly bounded by the uniformly positive primal Gram
matrix, while (1) at a strict-left node has its O(p_{k,j}) factor. Thus (2),
(3), the bounds on E, and their errors hold uniformly for small eta. The
augmented hatted extra root is now its leftmost root.

## 3. Uniform error at the displacement scale

Use the same Rayleigh trial as agent3's exact argument, namely the next hatted
polynomial divided by x-a_{k+1}(eta). Let

    mu_i=qhat_{k,i} Hhat_k(lambda_i)^2,
    R_E=sum_i E_i mu_i lambda_i/(lambda_i-a)^2
        /sum_i E_i mu_i/(lambda_i-a)^2,
    R_1=the same quotient with E identically one,

where a=a_{k+1}(eta). Scalar normalizations cancel. The only spectral node
within fixed distance of zeta is the probe itself. By (3), at every original
node mu_i is uniformly bounded, and its strict-left part is O(rho^k). At the
probe mu_zeta is comparable to eta, since q_zeta is comparable to eta^-1 and
Hhat_k(zeta) is comparable to eta alpha_k. Consequently the denominator of
each quotient is comparable to eta^-1.

CRUCIAL: subtract zeta before estimating the numerator:

    R_E-zeta = [sum_i E_i mu_i(lambda_i-zeta)/(lambda_i-a)^2]
               /[sum_i E_i mu_i/(lambda_i-a)^2].              (4)

The probe's numerator term is EXACTLY ZERO. Therefore each numerator is O(1),
the numerator difference is O(rho^k), and the denominator relative difference
is O(rho^k). (At strict-left nodes use small mu and bounded E; elsewhere use
E=1+O(rho^k).) Equation (4) yields

    R_E-R_1=O(eta rho^k),                                    (5)

uniformly on the tail. An O(rho^k) estimate without the eta factor would NOT
suffice; (4) is what gives the required factor.

The Rayleigh bound and agent3's unperturbed first-order calculation now give

    alpha_{k+2} <= alpha_{k+1}^2/alpha_k + O(rho^k)

with the current-weight triple normalization, whose alpha's are uniformly
nonzero and bounded. Therefore, writing beta_k for the exact common-parameter
ratio, one obtains

    sign(alpha_k)*(log beta_{k+1}-log beta_k) <= C rho^k.       (6)

The signs are fixed on the tail. If beta_k -> beta_infinity>0, summing the
geometric tail of (6) gives

    sign(alpha_k)*(log beta_k-log beta_infinity) >= -C' rho^k. (7)

This is precisely the exponentially perturbed virtual-root inequality needed
in the lower-s=3 proof. All limits in eta were taken separately at fixed
finite triples; uniform estimates were needed only for the explicit error
coefficient in (5), and were established above.

## 4. Comparison with deficit

In a hard case with an active negative-neutral outsider, sum t_k=infinity
and t_{k+1}/t_k ->1. Thus rho^k=o(t_k). Dividing (7) by t_k leaves the same
limiting signed inequality as if there had been no strict-left spectral nodes.
This applies at every fixed zeta<c; the subsequent zeta -> c limit is handled
by agent4's general-zeta/P_5(zeta) calculation (including P_5(c)=0).
