# General scalar-dual flip-mode identities

Fix an m=s+2-node two-cycle with monic polynomials P,Q, monic characteristic D, norm C=H^2, and monic dual f(x)=x-t. Its weights are
 w_i=C(lambda_i-t)/(D'(lambda_i)P(lambda_i)),
 z_i=C(lambda_i-t)/(D'(lambda_i)Q(lambda_i)).
Thus G_w(x)=f(x)Q(x)/D(x), G_z(x)=f(x)P(x)/D(x), where G_w=sum w_i/(x-lambda_i). In particular
 A_w=sum w_i/(lambda_i-t)^2=-Q(t)/D(t),
 A_z=sum z_i/(lambda_i-t)^2=-P(t)/D(t).

Choose normal frame u_i=w_i P_i h(lambda_i), deg h<s. Let F=delta(H^2) and let v be the two-step tangent drift of t. The variation of the dual root under u is delta t. Exact differentiation of the dual weighted mean, and sum w_i P_i h_i/(lambda_i-t)=0 (orthogonality plus barycentric sum), give delta t_next=2 delta t and v=2 delta t. Hence
 v=-2 sum z_i P_i h_i/(lambda_i-t)/A_z.

Add a missing spectral node mu with P(mu)Q(mu)=-C. If its residual amplitude is epsilon A_mu, the outside weight is epsilon^2 A_mu^2. The normal force in the moving frame is
 hdot_mu=(4P(mu)/C) M_z^{-1} V(mu) A_mu^2,
 where M_z=sum z_i V_i V_i^T and V=(1,x,...,x^(s-1)).

The L2(z) projection of P(x)/(x-t) onto degree<s polynomials is exactly
 [P(x)-P(t)Q(x)/Q(t)]/(x-t).
Indeed after subtracting, the remainder is P(t)Q(x)/(Q(t)(x-t)); its inner product with any test polynomial is zero, by division by x-t, Q-orthogonality, and sum z_i Q_i/(lambda_i-t)=C sum 1/D'_i=0.

Applying the velocity functional to hdot_mu yields
 vdot_force=8D(t)P(mu)[P(mu)Q(t)-P(t)Q(mu)]/[C P(t)Q(t)(mu-t)] A_mu^2.
Equivalently, if K(t)=C v/(2D(t)) is the scalar-dual momentum evaluation,
 K(t)dot_force=4P(mu)[P(mu)Q(t)-P(t)Q(mu)]/[P(t)Q(t)(mu-t)] A_mu^2.

The unforced scalar-dual root acceleration is
 vdot=[D'/D - (P'/P+Q'/Q)/2] v^2.
One direct derivation uses exact scalar shift recurrence. With nu=I(w_k), f_k=x-t_k and delta=t_(k+1)-t_k,
 delta_next=delta [1+delta G_nu(t_(k+1))]/[sum nu_i(lambda_i-t_k)^2/(lambda_i-t_(k+1))^2],
 where nu is normalized and G_nu=sum nu_i/(lambda_i-t). Its Taylor expansion is delta_next-delta=-G_nu(t_k)delta^2+O(delta^3). At the cycle nu is proportional to z/(x-t)^2, so G_nu(t)=P'/P-D'/D. Pairing the two block parities swaps P,Q and gives the stated acceleration. Consequently J=K(t)sqrt(P(t)Q(t)) is conserved without flip modes, and in their presence
 Jdot=4 sum_mu A_mu^2 P(mu)[P(mu)Q(t)-P(t)Q(mu)]/[(mu-t)sqrt(P(t)Q(t))].

Finally, the fuel derivative is universally
 Fdot=-C(P(t)+Q(t))v^2/(4D(t)) + sum_mu 4(P(mu)^2+C) A_mu^2.
For the kinetic term use the sum Fisher metric C(A_w+A_z); for the force term use F's frame functional sum w_i P_i^3 h_i=C sum z_i P_i h_i and projection of P under z equals P-Q. Both kinetic and potential terms are nonnegative, strictly positive for nonzero velocity or amplitudes.

These identities concern the rigorously derived leading blow-up ODE. They do not by themselves establish existence of a nonconvergent orbit of the original discrete method.
