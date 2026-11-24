# Positive 5x5 linearization of a hard s=3 edge
Let f,g monic cubics, N>0, fg-N=P5(z)(z-c), and c<a<b is the hard dual gap. On [a,b], f,g<0 except that fg=N at endpoints; at c, f(c),g(c)>0 and f(c)g(c)=N. Put M(z)=[[g(z),-sqrt(N)],[-sqrt(N),f(z)]].

Etheta(z)=M(z)/[(z-c)(z-theta)] is the matrix Nevanlinna function
 z I2-Dtheta-Vc/(z-c)-Vtheta/(z-theta),
 Dtheta=diag(-g2-c-theta,-f2-c-theta),
 Vc=M(c)/(theta-c)>=0 rank1,
 Vtheta=-M(theta)/(theta-c)>0 in the interior, rank1 at endpoints.
Moreover Vtheta'=Dtheta-theta I2+Vc/(theta-c).

Choose bc bc^T=Vc, bc'= -bc/[2(theta-c)]. Choose B B^T=Vtheta horizontally by B'=(1/2)Vtheta' B^-T (possible throughout open gap; this ODE preserves BB^T=Vtheta). Form the symmetric 5x5 block matrix
 Ltheta=[[Dtheta,bc,B],[bc^T,c,0],[B^T,0,theta I2]].
Schur complements give det(zI5-Ltheta)=(fg-N)/(z-c)=P5(z); it is an explicit positive isospectral family with fixed spectrum the five base nodes. At either gap endpoint B has rank one, so one uncoupled endpoint eigenvector splits off, leaving the minimal four-node Jacobi-type realization.

Set skew K with nonzero blocks
 K(port,theta)=-B^-T/2,
 K(theta,c)=B^-1 bc/[2(theta-c)],
and their negative transposes. Direct block multiplication proves Ltheta'=[K,Ltheta]. Thus this particular horizontal lift is transported orthogonally.

All decomposition and Lax identities checked EXACTLY with generic SymPy symbols in agent1_lax_family_checks.py. This is a rigorous structural lemma, NOT YET a proof identifying the normal w-flight connection with a positive channel transport, nor the desired cooperative kernel inequality.
