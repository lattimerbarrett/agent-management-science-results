# Codimension-two avoidance implies an attracting entire chart (proved)
Let n>=3, let K be compact in C^n, and let p lie on an affine complex (n-2)-plane L disjoint from K. There exists an injective entire map Phi:C^n→C^n minus K with Phi(0)=p and invertible derivative everywhere.

Move p to zero and L to {x=y=0}; write coordinates (x,y,z_1,...,z_{n-2}). Put a=1/2. Set
H(x,y,z_1,z_2,...)= (a y+M x², a z_1+M y², a x, a z_2,...).
This is a polynomial automorphism: solve successively x=z'_1/a, y=(x'-Mx²)/a, z_1=(y'-My²)/a, z_j=z'_j/a. Its derivative at zero is A=aP, P unitary (a 3-cycle plus fixed coordinates).

Take R>=1 bounding the absolute values of all coordinates on K, and delta=min_K max(|x|,|y|)>0. Choose M=2+(4R+4)/delta². The first image of K has foreground maximum r'=max(|x'|,|y'|)>=M delta²-aR=2delta²+3.5R+4, while all background coordinates have absolute value <=aR. Hence H(K) lies in
C={max(|x|,|y|)>max(2,2 max_j|z_j|)}.
On C, if r=max(|x|,|y|), then r_next>=Mr²-ar>2r, and background_next<=ar. Thus C is forward invariant and every point of H(K) escapes to infinity. The attracting basin B of zero is therefore disjoint from K.

For completeness, B is biholomorphic to C^n without invoking a separate basin theorem. Choose a<b<sqrt(a). For a sufficiently small neighborhood U of zero, ||H(x)||<=b||x|| and ||H(x)-Ax||<=C||x||². The maps phi_k=A^{-k}H^k converge uniformly on a smaller neighborhood because
||phi_{k+1}-phi_k||<=C a^{-1}(b²/a)^k ||x||².
The limit phi is holomorphic, Dphi(0)=I, and phi H=A phi. Shrink U so phi is injective and H(U) subset U. Extend phi to B by phi(x)=A^{-k}phi(H^k(x)) once H^k(x) lies in U. This extension is well-defined, holomorphic, and injective. Its image contains every A^{-k}phi(U), whose union is C^n since phi(U) contains a ball and A is a strict scalar contraction times a unitary matrix. Thus phi:B→C^n is biholomorphic. Its inverse, followed by the original coordinate change, is the asserted Phi.

Application: the compact mixed Hartogs domain K={(z,w):(|z|²-1)²+||w||²<=2}, z in C, w in C^{n-1}, has an avoiding affine (n-2)-plane through every exterior point. At a fixed base z, its nonempty fiber is a ball. Through any point outside that ball take the affine hyperplane in the w-space perpendicular to w; its norm is everywhere at least ||w||, so it avoids the ball. Empty fibers cause no problem. Therefore the exterior is strongly dominable everywhere.

This is NOT a CAP/Oka proof: no holomorphic family of the avoiding planes or charts along an arbitrary convex-source map has been constructed.
