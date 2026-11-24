# Four-node critical s=2 local convergence lemma

Let the distinct nodes be the four roots of P(x)=(x^2-c)^2-1, c>1, and let T be the degree-two residual weight map. Suppose an orbit w_{2k} approaches the critical fixed segment W on which the monic orthogonal polynomial is p(x)=x^2-c. Then w_{2k} converges.

The affine node normalization is harmless for normalized residual dynamics; every repeated-factor four-node critical configuration can be put in this form.

Proof. Write q=x^2-c-a-bx and mu=E_w x. Orthogonality gives E x^2=c+a+b mu and E x^3=c mu+a mu+b(c+a+b mu). Thus (mu,a,b) are analytic coordinates near W: the moment-coordinate Jacobian on W equals c-mu^2>0. On W, E x^2=c and E x^3=c mu. Let u=sqrt(c-1),v=sqrt(c+1). The total weight on each radius is 1/2. If d_u,d_v are the signed imbalances of the two radii, the second orthogonality condition gives v d_v=u d_u and mu=2u d_u. Consequently W is exactly -u<=mu<=u; in particular c-mu^2>=1 throughout W.

Put A=2a+b^2,B=b. Both hypersurfaces A=0 and B=0 are fixed point sets of F=T^2. Indeed when b=0, q(p+a)=P+1-a^2; when a=-b^2/2, q(x)(p+b^2/2+bx)=P+1-c b^2+b^4/4. The displayed companion polynomial is monic degree two. The constant-product identity plus q-orthogonality implies it is the monic orthogonal polynomial for T(w), and the constant is h(w). Thus T^2(w)=w. These identities are rational identities and hence extend to a whole coordinate neighborhood, not merely its positive-weight portion.

It follows by analytic divisibility that F has the form
 A_new=A[1+B f(mu,A,B)],
 B_new=B[1+A g(mu,A,B)],
 mu_new-mu=A B C(mu,A,B),
where f,g,C are analytic near W. The coordinate neighborhood may include signed weights; all moment and normalization denominators stay nonzero on W, so this analytic extension is legitimate.

The quadratic two-step expansion, verified symbolically in agent2_s2_local_checks.py, is
 mu_new-mu=4ab[(c-mu^2)^(-1)-(c-mu^2)]+O((|a|+|b|)^3).
Hence
 C(mu,0,0)=-2[(c-mu^2)-(c-mu^2)^(-1)]<0
for every interior point |mu|<u.

By assumption A,B tend to zero and mu approaches [-u,u]. The two bracketed multiplicative factors in the formulas for A_new,B_new are eventually positive uniformly near this compact segment. Thus each of A,B has eventually constant sign, unless one is zero, in which case the orbit is already fixed. On any compact subinterval of (-u,u), C is eventually negative. Therefore all sufficiently late increments of mu starting in that subinterval have one fixed sign. Since increments tend to zero, mu cannot cross this subinterval in both directions infinitely often. Two distinct cluster values of mu would force exactly these opposite crossings of an intervening compact interior subinterval. This contradiction proves convergence of mu, and hence of all weights by the coordinate formulas.
