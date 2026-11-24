# Conditional finite-cluster exclusion of interior Green poles

Let G>0 be harmonic on the upper half-space outside a finite nonempty set of
poles, with zero normal derivative on the boundary away from its boundary
poles. Suppose G occurs as a C2-local limit away from poles of smooth positive
solutions of Delta v_i+eta_i kappa v_i^p=0, eta_i->0, on domains converging
to the half-space, with vanishing Robin coefficients. At every interior pole,
assume its enclosing fixed spheres lie in the smooth-solution convergence
region, so passing the translation stress flux to the limit is legitimate.
Then G cannot have an interior pole.

Proof. Even reflection and Bocher's theorem, followed by bounded-below
harmonic Liouville after subtracting all finite singularities, give
 G(x)=sum_j a_j[|x-z_j|^(2-n)+|x-z_j*|^(2-n)]
       +sum_l b_l |x-w_l|^(2-n)+C,
where z_j=(z'_j,t_j), t_j>0, z_j*=(z'_j,-t_j), w_l lies on the boundary,
and a_j,b_l>0. Write G=a_j|x-z_j|^(2-n)+H_j near an interior pole.
Its translation stress flux equals (2-n)a_j omega_(n-1) grad H_j(z_j).
Every smooth approximating solution has zero flux through any enclosing
sphere, so grad H_j(z_j)=0 for every interior pole.

On the other hand, differentiating the explicit representation gives
 sum_j a_j partial_n H_j(z_j)
 = (2-n) sum_(j,k) a_j a_k(t_j+t_k)|z_j-z_k*|^(-n)
   +(2-n) sum_(j,l) a_j b_l t_j |z_j-w_l|^(-n).
The direct interactions between distinct interior poles cancel pairwise,
since their normal differences t_j-t_k have opposite signs. Each image term
is strictly negative, including the diagonal self-image term, and each
boundary-pole term is negative. Thus the sum is strictly negative whenever
there is any interior pole, contradicting its required zero value.

This lemma supplies only a conditional finite Green-cluster exclusion. It does
not establish that an arbitrary blowing-up solution sequence has a finite
pole limit with the convergence and normalization hypotheses stated above.
