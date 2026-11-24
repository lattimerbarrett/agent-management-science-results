# Single-negative monomial closes the hard cubic edge (agent 3)

Assume the hard s=3 configuration: P=prod_{i=1}^5(x-lambda_i),
fg=L+P(x)(x-c), and the only nonconstant limiting weight coordinate is
theta in [a,b], with c<a<b and d_a=P'(a)>0, d_b=P'(b)<0.
All active negative-neutral outsiders satisfy z>c. Let t_k=L-N_(2k).
The virtual-root lemma supplies, uniformly along the actual orbit,

    liminf I_k/t_k >= 0,

where A_k=-t_k and I is the canonical first-order linear functional
I=-(cA+B)+sqrt(f(theta)g(theta))*K/(theta-c).

For a fixed negative-neutral spectral node z, define the smooth-on-(a,b)
function Phi_z by

    Phi_z'(theta)=-(f(theta)g(theta)+L)
                  /[P(theta)(theta-c)(z-theta)].

The pole at theta=z cancels because f(z)g(z)+L=0. Only the poles at a,b
matter on the closed edge. Their residues are

    eta_a=2L/[P'(a)(a-c)(a-z)],
    eta_b=2L/[P'(b)(b-c)(b-z)].

Thus Phi_z=eta_a log(theta-a)+eta_b log(b-theta)+G_z(theta), where G_z
extends smoothly with bounded derivatives to [a,b]. This formulation also
handles c coinciding with another positive base node: its possible double
pole is strictly outside [a,b] and is absorbed in G_z.

If c<z<a, eta_a>0, eta_b<0, so Phi_z is a proper increasing bijection
(a,b)->R. If z>b, eta_a<0, eta_b>0, so it is proper decreasing.

## An actual exact-iteration scalar

On a sufficiently late even tail, factor the exact monic dual polynomial as

    H_k(x)=D_k(x)(x-theta_k),

where D_k consists of every root converging to a vanished outsider. All those
roots remain uniformly separated from [a,b]. Repeated eigenvalues were
already combined. Exact interpolation gives, for each base endpoint i=a,b,

    p_(k,i)=N_k D_k(lambda_i)(lambda_i-theta_k)/(d_i f_k(lambda_i)).

Here d_i is the derivative of the polynomial through ALL active spectral
nodes. Consequently

    p_(k,a)=C_(k,a)(theta_k-a),
    p_(k,b)=C_(k,b)(b-theta_k),

with C_(k,a),C_(k,b)>0 converging to nonzero constants, uniformly as theta
approaches either face. Moreover, over a two-block update,

    Delta log C_(k,i)=o(t_k), i=a,b.                              (1)

Indeed, Delta N and the even-polynomial coefficient change are O(t_k^2)
by the Lyapunov gain bound and polynomial TV. Strict-outsider dual roots
move exponentially. A negative-neutral dual root differs from its spectral
node by O(p_z)=O(t_k^2), and moves O(t_k p_z) over two blocks. A possible
positive-neutral outsider at c has root displacement O(p_c), p_c->0, and
moves O(t_k p_c)=o(t_k). These follow uniformly from the exact dual identity
H_k(lambda_i)=d_i p_(k,i)f_k(lambda_i)/N_k and simple-root implicit inversion.

Define the exact scalar

    Psi_k=log p_(k,z)+eta_a log p_(k,a)+eta_b log p_(k,b)+G_z(theta_k).

It differs from log p_(k,z)+Phi_z(theta_k) by a bounded scalar converging
to a constant. The canonical first-order identity is

    growth_z + Phi_z'(theta)*theta_dot =
       -4A/L+4I/[L(z-c)].                                      (2)

Equation (2), (1), and the analytic two-block map expansion imply uniformly,
INCLUDING theta arbitrarily close to a or b,

    Psi_(k+1)-Psi_k = 4t_k/L+4I_k/[L(z-c)]+o(t_k).               (3)

Uniformity of logarithmic Taylor remainders at faces follows from exact
face invariance: Delta theta has factors (theta-a)(b-theta), so relative
endpoint changes are O(t_k); their log-Taylor errors are O(t_k^2).

By liminf I/t>=0, (3) is >=2t_k/L eventually. A positive, nonannihilated
negative-neutral coordinate forces sum_k t_k=infinity: otherwise its exact
two-block logarithmic multiplier, O(t_k), would be summable and p_(k,z)
could not tend zero. Thus Psi_k->+infinity.

Since log p_(k,z)<=0, the bounded-difference identity forces
Phi_z(theta_k)->+infinity. Therefore theta_k->b if z<a, and theta_k->a
if z>b. Either conclusion gives convergence of the even weight vector.
In particular a bracketing pair of active negative outsiders is impossible.
This finishes the hard cubic edge as soon as the virtual-root liminf
inequality is fully justified with strict-left deflation.
