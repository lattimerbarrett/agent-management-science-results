# Full-mode lower-halfspace Schur lemma (proved)

Let r,R>0, d>0 and theta real. (The reverse-radii extension is proved below.) Put s=sqrt(d^2+r^2+R^2-2rR cos(theta)), D=d+s,
c=(R exp(-i theta)-r)/D, b=(R-r exp(i theta))/D. For Re z>0 let
x=r/(z+sqrt(z^2+r^2)), y=R/(z+d+sqrt((z+d)^2+R^2)), using positive-real square roots.
Then

    w(z)=sqrt(r*y/(R*x)) (1+x*c)/(1+y*b)

is holomorphic, nonvanishing except possibly numerator zeros, and |w(z)|<1 on Re z>0.
The square root exists holomorphically, because x,y never vanish on the simply connected RHP.

## Boundary calculation

Write x=rho exp(i phi), y=sigma exp(i psi), and define
Ax=r(rho^-1-rho)/2, Bx=r(rho^-1+rho)/2,
Ay=R(sigma^-1-sigma)/2, By=R(sigma^-1+sigma)/2.
On z=it, Ax cos(phi)=0, Ay cos(psi)=d, Bx sin(phi)=By sin(psi)=-t.
Also Bx^2-Ax^2=r^2, By^2-Ay^2=R^2, Ax,Ay>=0.
Let p=|c|^2=|b|^2=(s-d)/(s+d)<1. Define

    Delta = [ (R/|y|)|1+y*b|^2 - (r/|x|)|1+x*c|^2 ]/(1+p).

Using (1-p)/(1+p)=d/s and 2/((s+d)(1+p))=1/s gives exactly

    s Delta = s(By-Bx)+d(Ay-Ax)+R^2 cos(psi)+r^2 cos(phi)
            -rR cos(theta)(cos(psi)+cos(phi))
            +rR sin(theta)(sin(psi)-sin(phi)).                 (1)

We prove this is strictly positive at every finite t.

### Case |t|<=r

Here Ax=0, Bx=r, cos(phi)=q/r, q=sqrt(r^2-t^2).
Write B=By, u=Ay=sqrt(B^2-R^2), v=sqrt(B^2-t^2).
Then cos(psi)=v/B and d=u*v/B. In particular B>R>r.
Equation (1) is

    s Delta = A*s + K - L*cos(theta)+M*sin(theta),
    A=B-r>0, K=B*v+r*q,
    L=R*(r*v/B+q), M=R*t*(B-r)/B.

Let J=(r*v/B+q)^2+t^2*(B-r)^2/B^2 >=0. Then

    K^2-B^2*J=(B-r)^2*((B+r)^2-t^2)>0.

Since R<B, K^2>L^2+M^2=R^2*J and K>0. Thus s Delta>0.
The endpoints t=+-r follow from the same formula q=0.

### Case |t|>=r

Put T=|t|, E=sqrt(T^2-r^2). Then Ax=E, Bx=T, cos(phi)=0,
sin(phi)=-sgn(t). Again write B=By, u=sqrt(B^2-R^2),
v=sqrt(B^2-T^2). We have B>max(R,T), d=u*v/B.
Equation (1) is again

    s Delta=A*s+K-L*cos(theta)+M*sin(theta),
    A=B-T>0, K=(v/B)*(B^2-u*E),
    L=rR*v/B, M=rR*sgn(t)*A/B.

Cauchy-Schwarz for (u,R) and (E,r) yields uE+rR<=BT.
Consequently B^2-uE >= B*A+rR>0 and K>0. Moreover

    K^2-L^2-M^2
      = A/B^2 * [(B+T)*(B^2-uE)^2-2B*r^2*R^2]
      >= A^2/B^2 * [-r^2*R^2+2B*(B+T)*rR+B^2*A*(B+T)] >0,

because B>=R and T>=r imply B*(B+T)>rR.
Thus s Delta>0 in this case too.

## Holomorphic conclusion

The chosen x,y map their RHP arguments into {Re u>0, |u|<1}; hence
|y*b|<1 and the denominator has no zero. The boundary values of w are
continuous at the branch points +-ir. The strict boundary inequality
Delta>0 gives |w(it)|<1 at every finite t. At infinity in the closed RHP,
x~r/(2z), y~R/(2(z+d)), so w(z)->1 uniformly. Applying the maximum
principle to growing halfdisks gives |w|<=1 on RHP; the strong maximum
principle gives strictness, since its finite boundary values are <1.

This proves a scalar Schur function for every angular mode, including theta=0, initially when r<R.
It does NOT yet identify the Atiyah determinant with its Pick kernels.
The upper-halfspace function and arbitrary radii are addressed below.


## Strict Pick positivity (all distinct RHP nodes)

For the RHP Hardy space use boundary norm (1/(2*pi)) integral_R |f(it)|^2 dt
and Cauchy kernels k_z(t)=1/(it+conj(z)); their Gram matrix is
1/(z+conj(w)). Multiplication M_w by the Schur function above is a contraction,
and M_w^* k_z=conj(w(z))*k_z (Cauchy reproducing formula).
For any finite sum f of distinct Cauchy kernels,

    <(I-M_w M_w^*)f,f>
      = ||f||^2-||P_+(conj(w)*f)||^2
      >= (1/(2*pi)) integral_R (1-|w(it)|^2)|f(it)|^2 dt >0.

The last strict inequality holds for every nonzero f, because the boundary
defect is strictly positive at every finite t, and a nonzero rational f
cannot vanish on an interval. Here P_+ is the orthogonal Cauchy projection
onto the RHP Hardy space; its norm is at most one. Thus every finite Pick
matrix [(1-w(z_i)*conj(w(z_j)))/(z_i+conj(z_j))] at distinct RHP nodes is
STRICTLY positive definite. This does not need a finite-degree or genericity
assumption and follows solely from the proved boundary defect.


## Arbitrary radii: the missing inside-boundary case

The outside-boundary proof above never used r<R. In the inside-boundary case
By=B>R always. If B>r the previous proof applies without any relation between
r and R. If B=r, then A=0, J=4(r^2-t^2)>0, and
K^2-R^2 J=(B^2-R^2)J>0, again sufficient.

Only R<B<r remains. Put h=|t|, p=sqrt(B^2-t^2), q=sqrt(r^2-t^2),
a=r-B>0, k=R/B in (0,1), K=Bp+rq, U=rp+Bq. Then

    s Delta=G-a*s,
    G=K-k*(U*cos(theta)+t*a*sin(theta)),
    s^2=p^2+r^2+k^2*t^2-2*r*k*B*cos(theta).

For t!=0 use B=h*cosh(u), r=h*cosh(v), v>u>0,
beta=cosh(v-u)>1 and L=cosh((u+v)/2)/sinh((v-u)/2)>0.
One obtains the exact factorization

    (G^2-a^2*s^2)/(a^2*t^2)
      =(beta-k*cos(theta)) *
       [L^2+1-k*((L^2-1)*cos(theta)+2*L*sgn(t)*sin(theta))] >0.

The second factor is >=(1-k)(L^2+1)>0 by Cauchy-Schwarz, since
(L^2-1)^2+4L^2=(L^2+1)^2. Moreover

    K^2-U^2-t^2*a^2=a^2*((r+B)^2-t^2)>0,

so G>=K-k*sqrt(U^2+t^2*a^2)>0. Thus G>a*s.
For t=0, directly G=s^2, and s^2-a^2=2rB(1-k*cos(theta))>0,
so again G>a*s. This completes the arbitrary-radii proof.

This last factorization and the hyperbolic parameter reductions were proved
independently by agents 2 and 3. Exact checkers and full derivations:
`agent2_reverse_schur.{md,py}` and `agent3_schur_boundary.py`.

## Upper-halfspace Schur function

Define alpha=g_r(z+d), beta=g_R(z), Re z>0. The upper function is

    w_upper(z)=sqrt(r*beta/(R*alpha))*(alpha+c)/(beta+b).

Its denominator has no zero since Re beta>0 and Re b>0.
Reflect and swap the two rings: r'=R, R'=r, c'=-conj(b), b'=-conj(c),
x'=beta, y'=alpha. These are exactly the lower data for radii r',R' and
angle theta, because c'=(r exp(-i theta)-R)/(d+s).

For ANY complex x',y' on the common Joukowski curve the exact factor identity gives

    sqrt(R'*x'/(r'*y'))*(y'-b')/(x'-c')
       = exp(i theta)*sqrt(r'*y'/(R'*x'))*(1+x'*c')/(1+y'*b').

Apparent singularities on the left are removable by the right-hand formula.
The left-hand function is exactly conj(w_upper(conj(z))). The right-hand
function has modulus strictly below 1 by the arbitrary-radii lower theorem.
Hence w_upper is strict Schur too. Applying the same Hardy-space argument
proves strict positive definiteness of every finite upper-mode Pick matrix.

The lower/upper analytic Schur-Pick lemmas are now complete for all modes.
**The global Atiyah-matrix-to-Pick-kernel connection is still unproved.**


### Elementary finite-kernel version (no Hardy projection theorem needed)

For completeness the strict Pick argument uses only a contour integral.
Let k_i(t)=1/(it+conj(z_i)), let f=sum a_i*k_i and
 g=sum a_i*conj(w(z_i))*k_i. Integrating on a growing right halfcircle gives

    (1/(2*pi)) integral_R
      w(it)/[(it+conj(z_i))*(-it+z_j)] dt
       = w(z_j)/(z_j+conj(z_i)).

This is Cauchy's formula; the closing integral vanishes because w is bounded
and the rational factor decays quadratically. Consequently
conj(w)*f-g is orthogonal to every k_i, and hence to g. Therefore

    ||f||^2-||g||^2
      = integral (1-|w|^2)|f|^2 dt/(2*pi)
        + ||conj(w)*f-g||^2.

The left side is exactly the quadratic form of the Pick matrix, up to
harmless transpose/conjugation convention. The first term is strictly
positive whenever some a_i is nonzero: f is a nonzero rational function
with distinct poles -conj(z_i), while 1-|w(it)|^2>0 at every finite t.
This proves strict Pick positivity using just residues and the already
proved boundary norm inequality.
