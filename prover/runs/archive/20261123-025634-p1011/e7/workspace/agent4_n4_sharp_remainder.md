# Dimension-four sharp first remainder after the umbilicity rate

This is a conditional local estimate, not a full compactness theorem. Inputs: isolated-simple strong decay, local microscopic bubble convergence, and the already proved rate |A_i|² log R_i<=C from agent4_n4_umbilicity_rate.md. All estimates use one fixed small physical outer radius delta0; constants never depend on the later Pohozaev radiusr<delta0/2.

## 1. Graph and corrections

Set epsilon=M^−1, R=delta0/epsilon, U=(1+|y|²)^−1. In uniformly flat-normalized coordinates, the graph is

F(z)=epsilon f2(z)+epsilon² f3(z)+O(epsilon³|z|4),

with tr f2=0 and f2=(1/2)A[z,z]. The scaled mean curvature isO(epsilon²r). Strong decay gives w=M^−1u(epsilon y)<=C(1+r)^−2 and local C² convergence toU. Center normalizations are w(0)=U(0), D_z w(0)=0.

Let Phi2 be the quadratic correction in agent4_n4_log_proof.md. It satisfies L Phi2=0, L=Delta+24U², the exact first quadratic boundary source, and

|D^k Phi2|<=C|A|(1+r)^−1−k, k=0,1,2.

Its value and first tangential derivatives at0 vanish by angular degree2.

There is also a bounded cubic correction Phi3 satisfying L Phi3=0 and

partial_out Phi3=4f3/(1+|z|²)²−(Delta f3)/(3(1+|z|²)) at t0,
|Phi3|<=C, |D^k Phi3|<=C(1+r)^−k, k=1,2,
Phi3(0)=0, D_z Phi3(0)=0.

Here is its construction. Write f3=H3+|z|²L1. Its far homogeneous harmonic correction is the odd degree0 functionq from agent4_n4_green_umbilic.md. Cut q off near0. The remaining volume residual isO(r^−4) and boundary mismatchO(r^−3), both energy-dual. In angular degree3 the Jacobi form is coercive. In angular degree1 it is coercive after removing the translation kernel, and the forcing is compatible with that kernel: for f3=|z|²z1 the exact boundary forcing is (2/3)(r²−5)z1/(1+r²)², whose pairing with Z1 is a constant times∫_0^infinity r4(r²−5)/(1+r²)4dr=0 by the beta identityI6=5I4. Cutoffq adds a variational residual with the same compatibility, because its infinity Wronskian withZ1 vanishes. Lax-Milgram on the complement constructs eta inD^{1,2}. Its preliminary O(r^−1) annular estimate, followed by the Neumann Newton representation, improves it toO(log(2+r)/r²), with gradientO(log(2+r)/r³). Thus Phi3=q+eta is bounded. Add translation kernel functions to set D_zPhi3(0)=0; oddness already givesPhi3(0)=0.

## 2. Extension into the thin negative-t strip

For either correction extend by

Phi(z,t)=Phi(z,−t)+2t b(z), t<0, b=partial_tPhi(z,0).

It isC² across the plane. The needed strip satisfies |t|<=C(epsilon|A|r²+epsilon²r³)<=Cdelta0 r. The additional linearized residual is2t(Delta_z b+24U²b). Since b2=O(|A|r^−2), Db2=O(|A|r^−3), Delta b2=O(|A|r^−4), while b3=O(r^−1), Delta b3=O(r^−3), this gives exactly the source bounds below.

## 3. Quantitative residual of the approximation

Put V=U+epsilon Phi2+epsilon²Phi3 on the curved halfball. Taylor expansion of the exact Euclidean boundary normal and the graph formula, together with the preceding strip extension, gives volume residual and boundary residual bounded respectively by sums

volume: C[epsilon²|A|²(1+r)^−2+epsilon³(1+r)^−1+epsilon4]
        plus integrable termsO(epsilon²(1+r)^−4),
boundary: C[epsilon²|A|²(1+r)^−1+epsilon³].

Every power is explicit: quadratic graph times first quadratic correction produces the |A|² terms; cubic and higher graph jets give the epsilon³ terms; the epsilon²Phi3 strip extension givesepsilon4. Nonlinear terms24U(epsilonPhi2+epsilon²Phi3)²+8(epsilonPhi2+epsilon²Phi3)³ have mixed-Green potentialsO(epsilon²): the worst extra logarithm isepsilon4 logR=o(epsilon²). Outer comparison values have sizeO_delta0(epsilon²) by strong decay and the correction bounds.

The first volume and boundary terms have Newton potential at mostCepsilon²|A|² logR=O(epsilon²) by the rate input. The next terms have potentialO(epsilon³R)=O(epsilon²delta0), and the last has potentialO(epsilon4R²)=O(epsilon²delta0²). Thus the entire mixed-Green lift of the residual isO_delta0(epsilon²).

## 4. Uniform sup bound for the remainder

Let h=w−V. For delta0small, V ispositive andcomparable toU since epsilonPhi2/U=O(|A|epsilon r) andepsilon²Phi3/U=O(epsilon²r²). Hence the exact divided-difference equation is

Delta h+c_i h=−residual(V), 0<=c_i<=C(1+r)^−4,
partial_out h=−(H_scaled/3)h−boundary_residual(V).

The mixed Neumann/outer-Dirichlet Green kernel is bounded byC|x−y|^−2 with uniform constants. Its exterior potential operator for(1+r)^−4 has norm<=C/R0², and the Robin perturbation has norm<=Cepsilon²R²=Cdelta0². Consequently, withE=||h||infinity,

E<=C_delta0 epsilon²+C(R0)sup_{r<R0}|h|+(C/R0²+Cdelta0²)E.

IfE/epsilon² wereunbounded, h/E would converge locally to a bounded Jacobi function with homogeneous Neumann data and zero value/tangential gradient at0. Every bounded n4 Jacobi function has expansionC+O(logr/r²): write it as the Neumann Newton potential of24U²h plus a bounded Neumann harmonic constant. Its Wronskian with the scale mode forcesC=0. It then has finite Dirichlet energy; stereographic transfer identifies it with the translation/scale kernel. The center constraints kill that kernel. Thus the compact sup term divided byE tends0; choosingR0large anddelta0small contradicts the displayed inequality. Therefore

|h|<=C_delta0 epsilon².

## 5. Gradient bound

Once the uniformO(epsilon²) value bound is established, ordinary annular boundary gradient estimates suffice; there is no need to differentiate a singular kernel. On an annulus of radiusr>=1, dilate by r. The graph has uniformly bounded small slope andC²norm, the Robin coefficient after dilation isO(epsilon²r²)<=Cdelta0², and all source Holder norms obey the same displayed polynomial bounds. The scaled boundary gradient estimate gives

|Dh|<=C[sup|h|/r+r sup|residual_volume|+sup|residual_boundary|]
 <=C[epsilon²/r+epsilon²|A|²/r+epsilon³+epsilon4r]
 <=C_delta0 epsilon²/r,

becauseepsilon r<=delta0 andAisbounded. The potentialc_i h is included sinceitscoefficient after dilation isO(r^−2). Local estimates onr<=2 giveO(epsilon²). Thus forr<R/2,

|Dh|<=C_delta0 epsilon²/(1+r). SincePhi3isbounded andDPhi3=O((1+r)^−1), we obtain the useful final form

|w−U−epsilonPhi2|<=C_delta0 epsilon²,
|D(w−U−epsilonPhi2)|<=C_delta0 epsilon²/(1+r).

These estimates are conditional only on the listed strong-decay and umbilicity-rate inputs. Applying them in the exact Robin stress identity still requires a separate accounting of parity, edge fluxes, and coordinate caps; that SP calculation is not asserted in this file.
