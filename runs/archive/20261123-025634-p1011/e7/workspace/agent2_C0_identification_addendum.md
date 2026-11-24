# Direct identification with the physical shape Hessian


The coefficient identification need not rely on an informal appeal to conformal invariance. Let L=E0''(U), S=J1'(U), and let W solve LW=-S. Put G=f U_t. Under the graph flattening diffeomorphism, the fixed ambient Euclidean bubble pulls back to
U(z,t+mu f(z))=U+mu G+(mu^2/2)f^2 U_tt+o(mu^2).
For a compactly supported graph deformation, its physical-domain energy has zero second derivative: the bulk density is even in t, so integrating from0 to mu f contributes only odd powers; H d_sigma has no quadratic term, while U(z,mu f)^2 has no linear term because U_t(z,0)=0. Therefore Taylor expansion in graph coordinates gives the exact identity
J2(U)+S(G)+(1/2)L(G,G)=0.
The first derivative E0'(U) annihilates the second-order function term. For the polynomial degree4 graph, pass to the compact cutoff limit. G belongs to D^(1,2) for n>8, and f^2 U_tt belongs to D^(1,2) for n>14, so all pairings and expansions above converge for n>=32 by the same weighted estimates already proved.

Using S(G)=-L(W,G), the reduced coefficient becomes
F=J2-(1/2)L(W,W)=-(1/2)L(W-G,W-G).
The function W-G is precisely the correction when the ambient fixed bubble, rather than the pulled-back bubble, is used as the reference ansatz. Its interior equation is homogeneous Jacobi, and its boundary normal derivative is the first Robin defect of the ambient bubble. Stereographic transfer therefore gives exactly the hemisphere Neumann problem used in the spectral shape-Hessian lemma. The unit-radius normalization changes F only by a common positive factor 2^(-(n-2)), not by any parameter-dependent term.

Changing the projected complement changes W by a Jacobi kernel element only, because S annihilates that kernel. Since L vanishes when either argument is in its kernel, F and the displayed norm are unchanged. This closes the projection-gauge issue in identifying the C0 coefficient with the certified spectral minimum.
