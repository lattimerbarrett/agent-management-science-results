# Compression proof for the interlacing polynomial B

Let n=2s, let y0,y1,y2 be three successive normalized residuals in the sign convention y1=q(A)y0/sqrt(h), y2=qnext(A)y1/sqrt(hnext) (the harmless common (-1)^s factors do not change spaces), and let P(z)=prod_i(z-lambda_i). Let M,Mnext,Mnextnext be their Stieltjes numerators. Divide qM=aP+t and qnext Mnext=anext P+tnext. Then Mnext=q t/h and a tnext-anext t=q B, where deg B<=s-2 and its leading coefficient is K=hnext-h>=0.

Suppose K>0. Put F=q qnext and w_i=y0_i^2. Orthogonality gives E_w F=h, E_w F^2=h hnext. Define S(z)=E_w[1/(z-lambda)], U(z)=E_w[F/(z-lambda)], V(z)=E_w[F^2/(z-lambda)]. Since (qnext(z)-qnext(lambda))/(z-lambda) has degree s-1 in lambda,
 U(z)=qnext(z)t(z)/P(z),
 V(z)=h qnext(z)tnext(z)/P(z).
Consequently
 S(z)V(z)-U(z)^2 = h qnext(z) B(z)/P(z).

The left side is det(X^T(zI-A)^(-1)X), where X has columns y0 and F(A)y0. By the compression determinant identity,
 P(z) det(X^T(zI-A)^(-1)X)=det(X^TX) det(zI-A_C),
where C=span{y0,F(A)y0}^perp=span{y0,y2}^perp and A_C denotes orthogonal compression. Here det(X^TX)=hK. Thus
 det(zI-A_C)=qnext(z) B(z)/K.

The subspace K_s(A,y1) lies in C: y2 is orthogonal to it by the minimization, and y0 is orthogonal to it by symmetry of A and the previous minimization. It is invariant under A_C, because A^s y1 belongs to K_s(A,y1)+span{y2}. Its characteristic polynomial for the compressed operator is qnext. Hence B/K is the characteristic polynomial of the compression to
 W=(K_s(A,y1)+span{y0,y2})^perp.

Now L=(K_s(A,y1)+span{y2})^perp has dimension s-1. The same invariant-subspace argument inside y2^perp shows that its compression has characteristic polynomial tnext/hnext. Moreover W is a codimension-one subspace of L, since K>0 means y0,y2 independent. Cauchy interlacing therefore proves that the s-2 roots of B interlace the s-1 roots of tnext. In particular, for s=3 the unique root of B lies between the two NEW Dirichlet poles. For s=2, B=K is positive constant.

The same proof works for general n, with deg B=n-s-2, dim L=n-s-1. It does not itself solve the extra-mode issue, since the poles corresponding to the limiting core need not be the outermost poles of tnext.
