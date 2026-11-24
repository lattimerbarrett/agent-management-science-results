# Pure-red structure of red-loop rows below the homogeneous boundary

Let (X,mu) have total measure one. Suppose 0<a<=1/4 and f,g:X->[0,1] satisfy integral f^2<=a and integral g^2<=a. Then

  integral (1-f)(1-g) >= (1-sqrt(a))^2.

Proof. Write s=sqrt(a), d=integral g<=s. By Cauchy-Schwarz,

  integral (1-f)(1-g)
  =1-d-integral f(1-g)
  >=1-d-s sqrt(integral (1-g)^2)
  >=1-d-s sqrt(1-2d+a).

The last expression has derivative -1+s/sqrt(1-2d+a)<=0 on 0<=d<=s<=1/2: indeed 1-2d+a>=a. Thus it is at least its value at d=s, namely (1-s)^2. Every step is non-strict and hence valid at a=1/4 too.

Apply this to any two red-loop rows of a symmetric density matrix/graphon. Their squared red row norms are <=a. If their edge has any blue density, the blue book constraint would require their blue row inner product to be <=b. Therefore if b<(1-sqrt(a))^2, the edge must be pure red. All red-loop vertices consequently induce a pure-red clique.

If their total weight is rho, each such row has red squared norm at least rho, whence rho<=a. Its squared norm restricted to the blue-loop part is <=a-rho and its red degree is at most

  rho+sqrt((1-rho)(a-rho)).

For rho>0,a<1 this is strictly less than sqrt(a): expand squares, or use strict Cauchy-Schwarz on its own pure-red portion. This strengthens the ordinary red/blue loop degree separation but does not yet eliminate the red-loop mass.

Algebra and 2800 weighted random pairs checked by mixed_red_clique_checks.py.
