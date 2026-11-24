# General-probe virtual-root constraint, including P5(c)=0

This supplements agent3_virtual_root_lemma.md. It avoids dividing by P5(c), so
covers the repeated-positive-level-root case c in the five-node support.

Use N for the limiting monic squared norm, P=P5, Q(x)=x-c,
F(x)=f(x)g(x)=N+P(x)Q(x). We consider even cluster states normalized by
t=N-N_k, with limiting polynomial perturbation w, first norm variation A=-1,
first partner variation dg, and slow-root two-block velocity v.
Write

    R(x)=g(x)w(x)+f(x)dg(x)-A.

Dual interpolation, to first order, gives

    R(x)=C P(x) - (N v/2) * [1-P(x)/P(theta)]/(x-theta).          (1)

In particular H R=-Nv/2 on the base nodes. C is the leading x^5 coefficient.
For theta at an endpoint, read (1) and subsequent formulas by continuous
extension after the cancelling factor is removed. All expressions below are
smooth on a neighborhood of c because c is separated from the allowed
slow-root gap.

Take a fixed probe z<c sufficiently close to c, avoiding every original node.
Choose it below all non-strict limiting dual roots. An active positive outsider
at c has a dual root tending to c and is therefore above z. Strict-left dual
roots are removed as described in agent2's deflation lemma.

Give the probe initial weight eta, and let its added dual root be

    a_k(eta)=z+eta d_k+O(eta^2).

For each fixed k the exact dual interpolation identity gives

 d_k=-P_active(z)*u_k(z)*f_k(z)/(N_k H_k(z)),

where u_k(z)>0 is the linearized probe weight. In the S5 limit,
P_active(z)/H_k(z) tends P(z)/(z-theta), since every outside node factor
cancels its limiting dual-root factor. This remains true if an active positive
outside node is c; first fix z<c and then let k tend to infinity. Therefore

    sign(d_k)=sign(P(z))                                      (2)

on a tail, because f(c),g(c)>0 and theta>c. No value of P(c) is used.

The finite-triple Rayleigh expansion gives d_{k+2}<=d_{k+1}^2/d_k. Hence the
positive ratios r_k=d_{k+1}/d_k decrease if P(z)>0 and increase if P(z)<0.
Their common limit is rho(z)=F(z)/N>0. With exponentially deflated strict-left
nodes the same conclusion has an O(r^k) error, r<1. Consequently

 sign(P(z))*[log r_k-log rho(z)] >= -O(r^k).                    (3)

The exact ratio is

 r_k= f_k(z)f_{k+1}(z)/N_{k+1} * H_k(z)/H_{k+1}(z).            (4)

Fast outside dual roots contribute o(t) to its logarithmic variation: negative
outsiders have p=O(t^2), an active positive c outsider has root displacement
increment O(t p_c)=o(t), and strict outsiders are exponentially small=o(t).
The slow dual factor x-theta contributes -v/[2(theta-z)]. Thus at any even
normalized cluster state,

 [log r_k-log rho(z)]/t ->
       (R(z)+A)/F(z)-A/N-v/[2(theta-z)] =: L(z).               (5)

Here (3) applies along the full orbit before extracting the cluster state, so

    sign(P(z))*L(z)>=0.                                      (6)

Substitute (1) into (5), noting F-N=PQ. Cancellation yields the exact identity

 L(z)/P(z) = 1/F(z) * [ C-A*Q(z)/N
                  +v/(2(z-theta))*(Q(z)+N/P(theta)) ].       (7)

Since P(z) != 0, (6) says **the right-hand side of (7) is nonnegative**.
Now let z increase to c, avoiding the finite set of nodes. The right-hand side
is continuous there even if P(c)=0, and its limit is

    C/N + v/[2(c-theta)P(theta)] = I/N^2,

where the canonical resource is

    I=q_w(c)/(theta-c)
     =N*C+N^2*v/[2(c-theta)P(theta)].                          (8)

Identity (8) follows either by polynomial remainder or by the canonical
(A,B,K) formulas. Thus I>=0 at EVERY deficit-normalized cluster state,
INCLUDING P(c)=0. Equivalently I_actual >= -o(t).

## Why no hidden c-factor changes the sign

If c is an active outside node (not one of the five base nodes), both
P_active(z) and the limiting H_k(z) have a factor z-c; their ratio cancels it,
leaving P5(z)/(z-theta). If c is itself one of the five base nodes, its factor
occurs in P5 and is NOT cancelled. In both cases (2) is exactly sign(P5(z)).
For P5(c)=0, use (7) BEFORE taking z to c, never the vanishing expression
P5(c)*I. This is the essential order of limits.
