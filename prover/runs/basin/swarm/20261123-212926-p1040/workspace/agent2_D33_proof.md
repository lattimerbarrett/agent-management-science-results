# Unconditional elementary certificate: (3,3) belongs to D

Use the LEFT Magnus automorphisms K_ij:xi->xj xi xj^{-1} and M_i;jk:xi->[xj,xk]xi. Put A=M_3;12, B=M_1;23, C=K_12 and W=[[A,B],C]. Then W belongs to gamma3 IA3.

## W lies in A4

Write X=X1,Y=X2,Z=X3. Degree1 Johnson derivations are
 A(Z)=[X,Y], B(X)=[Y,Z], C(X)=[Y,X], zero on the other letters.
Their bracket E=[A,B] is
 E(X)=-ad(Y)^2 X, E(Y)=0, E(Z)=ad(Y)^2 Z.
It commutes with C, as checked on X,Y,Z. Thus tau3(W)=[[A,B],C]=0. Since gamma3 IA3 is contained in A3, the kernel property of tau3 yields W in A4. The companion checker additionally computes the actual free-group automorphism W and verifies every W(xi)xi^-1 has Magnus expansion 1 through tensor degree4.

## An actual group quotient detects W modulo gamma4

Use row Fox Jacobians abelianized at the character t=(1,-1,1). Every IA automorphism fixes this character. The fundamental Fox identity says J(phi)*(0,-2,0)^t=(0,-2,0)^t, so the row cycle module span(e1,e3) is invariant. The Fox chain rule in right-to-left automorphism composition is J(phi psi)=J(psi)J(phi). Therefore psi(phi)=(J(phi)|cycles)^-1 is a genuine homomorphism IA3->GL2(Z).

Direct Fox differentiation gives the generator images:
 K12 -> D=diag(-1,1), K32 -> -D;
 M1;23 -> U=[[1,2],[0,1]], M3;12 -> V=[[1,0],[-2,1]];
 all other standard Magnus generators -> identity.

Let H0=<D,U,V>. The pair U,V freely generates a free group: on the real projective line, put P={|x|>1}, Q={|x|<1}. Every nonzero power U^m sends Q into P, and every nonzero power V^m sends P into Q, because |x+2m|>1 for |x|<1 and |x/(1-2m x)|<1 for |x|>1. Ping-pong proves freeness, including faithfulness in PSL2, so -I is not in <U,V>. Also D^2=1 and DUD=U^-1, DVD=V^-1. Determinants distinguish D<U,V> from <U,V>, so H0 is exactly F(U,V) semidirect C2 with inversion on both free generators. On putting a=D,b=UD,c=VD, its presentation is <a,b,c | a^2=b^2=c^2=1>, the free product of three order-two groups.

The entire Fox image is H0 times the central group <-I>: K32=-D, while no -I belongs to H0 (determinants rule out its D-coset and ping-pong rules out its free subgroup). Consequently projection killing -I gives an actual homomorphism IA3->H0.

Now map this free product into UT4(F2) by
 a -> I+E12, b -> I+E23, c -> I+E34.
All three are involutions, so the map exists. It takes U=ba and V=ca. Exact matrix multiplication gives
 [[V,U],D] -> I+E14 != I.
The group UT4(F2) has nilpotency class at most3 (strictly upper triangular ideal has fourth power zero), hence gamma4 of this target is trivial. Therefore W is NOT in gamma4 IA3.

Together W in gamma3 IA3 intersection A4 but W notin gamma4 IA3 proves (3,3) in D. No conjectural IA presentation is used anywhere.

Every finite computation above is executed by `workspace/agent2_D33_certificate.py`, which uses only the Python standard library and runs in0.1sec.
