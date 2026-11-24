# Complete mixed-triangle inequality (computer-assisted algebraic certificate)

Let a in [1/12,1/9]. Let a probability space be partitioned into R,V0,V1,V2 of measures r,theta0,theta1,theta2. Write s=1-r, suppose 0<=r<=a, and let fi:X->[0,1] satisfy fi=0 on Vi. Suppose

  <fi,fj><=a (i!=j),  ||1-fi||^2<=b,
  sum_i theta_i int_R fi^2 <= r(a-r).

Then, putting c=1-b,

  c <= max{ 4 sqrt(a/3)-2a, 2 sqrt(a)-a }.

All inner products are with respect to the full probability space. This lemma uses only the stated finite moments, not any unproved regularization or symmetrization.

## Easy endpoint cases
Put p=sqrt(3a). If p=1/2, then for F=f0+f1+f2,
3c <= int(2F-F^2)+2 sum_{i<j}<fi,fj> <=1+6a=3/2.
If r=0 and p>=1/2, the quadratic H below has at most two active coordinates everywhere and directly gives c<=4p/3-2p^2/3.
Thus assume p>1/2 and r>0.

## Dual with a small adaptive correction
Let h=sqrt(3), x_i=theta_i/s, delta_i=x_i-1/3, and set

  tau=s(1-p)/p,  nu=(p+h-2)/(p s),
  mu_ij=2tau/3+r delta_k,  {i,j,k}={0,1,2}.

Here mu_ij>=0 and nu>0. Indeed p<=1/sqrt(3), r<=1/9 ensure 2tau>r. Also tau+r<1 because p>1/2.
Let T be the symmetric 3x3 matrix with diagonal 1/3 and off-diagonal mu_ij/2, and let M=T+nu diag(theta).

Both T and M are positive definite. To check T, use its affine dependence on the simplex point x. At each simplex vertex, 3T is a permutation of

  [[1,A,A],[A,1,B],[A,B,1]],
  A=tau-r/2, B=tau+r, 0<=A<=B<1.

One eigenvalue is 1-B>0 and the determinant of the remaining 2x2 block is 1+B-2A^2 >=1+B-2B^2>0. Convexity proves T positive definite for all x; adding nu diag(theta)>=0 gives the assertion about M.

Average the three inequalities c<=2 int fi-int fi^2, then add the nonnegative quantities mu_ij(a-<fi,fj>) and nu[r(a-r)-sum theta_i int_R fi^2]. Completing squares separately on R and the three Vi gives

 c <= F(p,r,x)
 := 2a tau+nu r(a-r)
    + sum_i (2theta_i/3)/(1+tau+(3r/2)delta_i)
    + (r/9) 1^T M^{-1} 1.                    (1)

For the Vi term, coordinate i is zero; the remaining 2x2 quadratic has equal diagonal 1/3 and off-diagonal between 0 and 1/3, so its maximum is exactly 2/[3(1+tau+(3r/2)delta_i)]. No box constraint or stationarity assumption is being silently used.

## Exact algebra proving the dual bound
We prove

 F <= max{4p/3-2p^2/3, 2p/h-p^2/3}.        (2)

All arithmetic below is in the ordered quadratic field Q(h), h^2=3,h>0. Write e2=sum_{i<j}xi*xj, e3=x0*x1*x2 and

 u=1-3e2, w=e2-9e3.

Nonnegative xi summing to one imply u>=0, w>=0, w<=u (Schur), and w<=(1-u)/3 (e3>=0). Therefore (u,w) belongs to the triangle with vertices (0,0),(1,0),(1/4,1/4).

Define A=2p, B=6(p+h-2), C=2s(1-p)-pr, D=3pr. The matrix N=6pM has diagonal A+Bxi and off-diagonal C+Dxk. Its determinant Q and the sum J of its adjugate entries are

 Q=A^3+A^2B+2C^3+2C^2D-3AC^2-2ACD-BC^2-AD^2-2BCD-BD^2
   +(AB^2+2CD^2+2AD^2+4BCD+3BD^2)e2 +(B^3+2D^3-3BD^2)e3,
 J=3(A-C)^2+2(B-D)(A-C)-D^2-2BD+(B+2D)^2 e2.

Also set d=2-2r+pr, e=3pr,

 U=d^3+d^2e+de^2 e2+e^3e3,
 V=d^2+2de e2+3e^2e3,
 L=2ps(1-p)/3+(p+h-2)r(p^2/3-r)/(ps).

Then the right side of (1) is exactly

 F=L+4psV/(3U)+2prJ/(3Q).

Q>0 and U>0 by the positive-definiteness/positive-denominator checks above.
For a proposed upper bound Z define

 P_Z=3ps(Z-L)UQ-4p^2s^2 VQ-2p^2rs JU
     =3psUQ(Z-F).

This is a polynomial in p,r,h,u,w modulo h^2=3, of degree at most two in (u,w). For Zm=4p/3-2p^2/3 it is divisible by r. The attached exact program proves

 P_Zm/r >=0 on p in [1/2,4-2h], r in [0,1/9], (u,w) in the above triangle;
 P_Zh   >=0 on p in [4-2h,h/3], r in [0,1/9], (u,w) in the above triangle,

where Zh=2ph/3-p^2/3. It does so as follows:

1. Expand in the six degree-two triangular Bernstein basis polynomials on (u,w).
2. For each of the six coefficient polynomials, substitute p=lo+(hi-lo)z and r=t/9.
3. Expand that polynomial in the rectangular Bernstein basis of degree (9,7) in the first range and (9,8) in the second.
4. Check every one of the resulting 6*80+6*90=1020 coefficients is nonnegative EXACTLY in Q(h), using rational arithmetic and squaring for signs.
5. Independently reconstruct every power coefficient from the Bernstein coefficients; also verify the triangular Bernstein identity, and generic determinant/adjugate identities.

All Bernstein basis polynomials are nonnegative on their defining rectangles/triangle. Hence these finite exact checks prove (2), including the transition endpoint, and thus prove the lemma.

The complete self-contained program is workspace/agent2_mixed_certificate.py. It has executed successfully (9.2 seconds); all 1020 exact coefficient checks and all independent reconstruction checks pass. It uses no floating-point arithmetic or external input files.
