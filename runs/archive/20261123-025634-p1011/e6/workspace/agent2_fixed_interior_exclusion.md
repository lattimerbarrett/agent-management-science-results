# Conditional exclusion of a fixed interior simple Green blow-up

Assume a positive-solution sequence blows up at an interior point p of a
positive-Yamabe compact LCF manifold M with nonempty smooth boundary. Assume
there is a normalization c_i->infinity such that c_i u_i converges in C2 on
compact subsets away from p to the normalized positive interior Green
function G_p (or to G_p plus a positive Green potential with other poles).
Then no such convergence is possible, using the standard spin positive-mass
theorem for an AF manifold with compact minimal boundary and its rigidity.

Proof. By conformal covariance choose a flat metric in a ball about p.
The critical Pohozaev vector has divergence zero, and the entire ball is
interior. Thus its spherical flux is exactly zero for every u_i and every
small radius. After multiplying by c_i^2, the nonlinear part vanishes on
fixed spheres, since q=2n/(n-2)>2 and c_i u_i has a finite smooth limit there.
The harmonic Green model is G=a r^(2-n)+A+O(r), a>0. Its full-sphere flux is
 -(n-2)^2 a A |S^(n-1)|/2.
Hence A=0.

On a finite spin cover of compact M, positive Yamabe type persists by the
ground-state identity. The single-interior-pole Green metric is complete,
scalar-flat and has compact minimal boundary. It is asymptotically flat
because the original metric is exactly flat in a neighborhood of the pole.
Spin PMT gives nonnegative mass; zero-mass rigidity would give Euclidean Rn,
which has no boundary, contrary to the nonempty boundary of M. Its mass is
therefore strictly positive. Lifted base Green is the sum of single-pole
cover Greens, so its regular coefficient is at least the strictly positive
cover coefficient. Consequently A>0, a contradiction. Any further positive
Green poles only add a positive smooth value at p and strengthen it.

Scope: isolated-simple decay, compact convergence under normalization and the
identification of the limit with a finite positive Green combination are
hypotheses, not established here. The input compact-minimal-boundary spin
PMT (or a suitable spin PMT applied to the minimal double) is explicitly used.
