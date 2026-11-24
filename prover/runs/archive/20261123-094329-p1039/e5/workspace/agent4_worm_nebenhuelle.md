# Elementary all-dimensional worm Nebenhülle obstruction

Use rho(z,w,zeta)=|z-exp(i log|w|^2)|^2-1+eta(log|w|^2)+||zeta||^2,
where eta=0 on [-mu,mu], mu>pi. Let K={rho<=0}.
Let r_-=exp(-pi/2), r_+=exp(pi/2), D={z:|z+1|<1}.
For every z in D the two circles
  (z,w,0), |w|=r_- or r_+
lie in int K, since their t-values are -pi,+pi, their centers both -1,
and eta=0. The annulus (0,w,0), r_-<=|w|<=r_+, lies in K.

Let U be any pseudoconvex open neighborhood of K. The component of U
containing K is Stein, and has a continuous psh exhaustion psi.
By compactness of the z=0 annulus there is s0 in (0,1/2) so the full
annulus at z=-s0 lies in U. Move z=-s continuously from s0 to 1/2.
Both boundary circles of every moving annulus stay in int K.
Their union is compact in U, hence psi is bounded above there by M.
For as long as a whole moving annulus lies in U, its restriction of psi
is subharmonic and the maximum principle bounds psi by M throughout it.
Thus that annulus lies in the fixed compact set {psi<=M} subset U.
At a hypothetical first exit time, compactness therefore keeps the limit
annulus inside U; openness extends past that time, a contradiction.
Consequently the whole annulus at z=-1/2 is in U, in particular
  p=(-1/2,1,0).
But rho(p)=5/4>0, so p is not in K.

Every pseudoconvex/Stein neighborhood of K contains this same exterior p.
Therefore K has no Stein neighborhood basis, in every ambient dimension.
This establishes only the Nebenhuelle obstruction, NOT exterior non-Oka.
The missing implication Oka exterior => Stein neighborhood basis has not
been proved and is not being asserted here.
