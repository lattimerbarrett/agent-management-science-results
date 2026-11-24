# Direct-scale replacement for the n4 umbilicity-rate proof

This addendum replaces the C¹ energy-remainder step in agent4_n4_umbilicity_rate.md with an exact identity. It also allows the simpler PHYSICAL correction model, avoiding material-coordinate terms. The conclusion and assumptions of that lemma are unchanged.

Let W_delta=chi(x)delta^−1U(x/delta) in local Euclidean Cartesian coordinates on the actual curved domain, and let

m_delta=chi(x)delta^−1[U(x/delta)+delta Phi2(x/delta)],

wherePhi2is the physical quadratic correction, extended through the thin negative-t strip as in the sharp-remainder proof. Projectm_delta−W_delta off the Jacobi span. The projection changes the model byo(delta) inH¹: flat angular orthogonality is exact, while the curved-domain strip changes the pairing byO(delta²(1+|A|²log(1/delta))). The inverse theorem holds for these Cartesian bubbles as well as for Fermi bubbles: their rescaled limits and Jacobi Gram matrices are identical, their potential operators differ byo(1), and the kernel projection perturbation iso(1). Equivalently repeat its rescaled contradiction proof verbatim.

The model residual isO(delta) inH*: the first quadratic boundary residual cancels; every remaining boundary source isO(delta²(1+r)^−1), whose dual-trace norm throughR=r0/delta isO(delta²R)=O(delta); the negative-strip extension volume source isO(delta²|A|²(1+r)^−2), whose L^{4/3} norm isO(delta²R)=O(delta); higherjets and nonlinear terms have the bounds already listed in the original rate proof. Cutoff errors areO(delta). Thus actual cut-off isolated-simple solutions andm_delta differ byO(delta) inH¹ after modulation, by the uniform projected inverse.

## Exact scale identity, no PDE assumption

For ANY smooth compactly supportedm in the Euclidean chart, let Tm=m+x·gradm. Direct differentiation of the critical bulk energy under m_s(x)=s m(sx), including its moving-domain Jacobian, gives

E'(m)[Tm]=∫boundary [(x·nu)(|gradm|²/2−2m4)+(H/3)m(m+x·gradm)].

There is no interior residual on the right and no approximation. The identity includes the boundary energy derivative2cHmv=(H/3)mv. Its sign can also be obtained from the divergence of the critical stress current.

For the explicitm_delta the first graph term (quadraticf2 against radialU) has zero angularmean. Its unique logarithmic term is the crossgradient withPhi2,

+(pi²/15)|A|²delta²log(r0/delta).

The Phi2² term, cubic/higher graph jets, actual-domain evaluation errors and all H terms contributeO(delta²): the same radial bounds as in agent4_n4_pohozaev_sign.md apply, except there is no unknownE. Cubicjet terms are odd and cancel; quartic and normalization errors have radialsize delta³R=delta²r0. The physical cutoff annulus has energy and scale pairingO(delta²). Therefore

E'(m_delta)[Tm_delta]=(pi²/15)|A|²delta²log(r0/delta)+O(delta²).

Let Z_delta be the cut-off scale Jacobi mode. The explicit model gives

||Tm_delta−Z_delta||H¹<=Cdelta[1+|A|sqrt(log(r0/delta))].

Indeed the difference isPhi2+x·gradPhi2 plus fixed-annulus cutoff terms. Pairing it against the O(delta) model residual costs at mostCdelta²(1+x), where x=|A|sqrt(log(r0/delta)). Consequently

E'(m_delta)[Z_delta]=(pi²/15)delta²x²+O(delta²(1+x)).

The actual cutoff solution residual paired againstZ_delta isO(delta²), since both the solution and the Jacobi mode areO(delta) on its fixed physical outer annulus. If eta is theO(delta) actual-minus-model correction, the linear difference pairedZ is bounded by ||eta|| times ||E''(W_delta)Z_delta||<=Cdelta²(1+x). The cubic nonlinear difference has the same bound, by ||m−W||<=Cdelta(1+x). Hence

(pi²/15)x²<=C(1+x).

This proves the rate without differentiating an unspecified asymptotic remainder. Constants are uniform under homothetic rescalings of the fixed manifold: its Q energy, projections and bubble operator are conjugated isometrically by the conformal scaling; shrinking cutoff radii were already treated in the inverse lemma.

The static addendum is not overwritten by running older checker files.
