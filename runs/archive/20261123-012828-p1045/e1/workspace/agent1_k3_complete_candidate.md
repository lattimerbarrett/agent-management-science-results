# Full k=3 greedy-partition moment inequality (agent1 candidate proof; audit pending)
Assume 1/12<=a<=1/9, b=1-c, c>max{1/2,g3(a),gh(a)}, where g3=4sqrt(a/3)-2a and gh=2sqrt(a)-a. Let R have measure r<=a, B measure s=1-r. Three profiles f_i:[0,1]->[0,1] satisfy blue norms<=b, pair inner products<=a. Suppose B is partitioned into V_i of measures theta_i such that f_i=0 on V_i and sum theta_i int_R f_i^2<=r(a-r). We prove contradiction c<=max(g3,gh).

## Universal theta cap
Put F=sum f_i,H=F-1,h=||H||. Let D_i=2<int f_i>-||f_i||²-c>=0 and e_ij=a-<f_i,f_j>>=0. Then
h²=1+6a-3c-sum D_i-2sum e_ij.
Also q_i=||f_i||²=c-4a+D_i+2sum_{j!=i}e_ij+2<f_i,H>, so
(sqrt(q_i)-h)²<=1+2a-2c.
Write p=sqrt(3a), t=(1-p)/p. Since c>=g3, h<=2p-1 and sqrt(q_i)<=x=2p-1+sqrt(B0), B0=1-8p/3+2p². Put E=1-2p/3,D0=E-g3=1-2p+2p²/3. All are positive for p in[1/2,1/sqrt3]. We have
sqrt(B0)+sqrt(D0)<=sqrt(2(B0+D0))<=sqrt(E)-(2p-1),
since the difference of squares in the second inequality is
2(2p-1)[(3-p)/3-sqrt(E)]>=0.
Therefore x<=sqrt(E)-sqrt(D0)<=sqrt(g3)<=sqrt(c). Since (u+c/u)/2 decreases for u<=sqrt(c),
d_i/sqrt(q_i)>=(sqrt(q_i)+c/sqrt(q_i))/2>=sqrt(E).
But f_i=0 on V_i gives d_i²<= (1-theta_i)q_i. Hence theta_i<=2p/3.

## A valid dual inequality
Let lambda=1/3. For tau,nu>=0 put
Q(z)=sum lambda(2z_i-z_i²)-2tau sum_{i<j}theta_k z_i z_j (k the missing index).
Let M_R have diagonal lambda+nu theta_i and offdiagonal tau theta_k.
If all relevant quadratic forms are PSD then
c <= 2a tau s + sum_i theta_i [2lambda²/(lambda+tau theta_i)] + r lambda² 1^T M_R^{-1}1 +nu r(a-r).
For singular PSD matrices use completing squares; the same displayed values are valid where specified below. This follows by subtracting weighted red-pair caps, maximizing pointwise on each V_i (coordinate i zero), and using the R energy budget. Nonnegative/box constraints can be dropped for upper bounds.

## Near-uniform partition
Normalize x_i=theta_i/s, let delta=x-(1/3,1/3,1/3), and assume max x_i<=1/(3t). Put nu0=sqrt3-1+(sqrt3-2)t, tau=t/s,nu=nu0/s. Then
B(x)=sum (2/3)x_i/(1+3t x_i), B0=2p/3,
R(x)=(1/9)1^T M^{-1}1, M=I/3+nu0 diag(x)+t offdiag(x_missing).
Concavity gives B0-B(x)>=t||delta||²/4.
Set beta=nu0-t,A=(1+t)/sqrt3. In the splitting span(1) plus its orthogonal complement, M has principal A, coupling beta delta/sqrt3, and perpendicular block C. If d=sqrt(1-3sum_{i<j}x_i x_j), then
lambda_min(C)=(1+nu0-t)/3-(2t+nu0)d/3.
Since max x<=1/(3t)<1/2, d<=1/t-1. Thus Cmin>=L(t)=[sqrt3-1+(2sqrt3-3)t-(sqrt3-1)/t]/3, increasing in t.
Schur complements give
R(x)-sqrt(a)=v/[3A(A-v)],  v=(beta²/3)delta^T C^{-1}delta.
If t>=sqrt3/2, L(t)>=1/(6sqrt3)>9/100, beta²<29/100, ||delta||²<2/125, hence v<1/50 and R-sqrt(a)<(2/5)||delta||².
If t<=sqrt3/2, L(t)>1/50, beta²<7/50, ||delta||²<9/100, hence v<21/100 and R-sqrt(a)<||delta||².
In both cases R-sqrt(a)<=8(B0-B), since t>=sqrt3-1>18/25. As r/s<=1/8, the full dual is at most its uniform-partition value
U=2at+2ps/3+r sqrt(a)+nu0 r(a-r)/s
 =g3+r(gh-g3)-nu0(1-a)r²/s<=max(g3,gh).

## Far partition
Let m=max x_i>1/(3t). The theta cap gives m<=2p/(3s), hence r>=2p-1. Choose tau=nu=1/(3sm). The B quadratic forms are PSD. The R matrix is I/3+T_x/(3m), where T_x has diagonal x_i and offdiagonal x_k. Its eigenvalues are 1,plus/minus d, with d<=m; therefore it is PSD and the R maximum is m/(1+m). Concavity in the other two x coordinates gives
c<=J(r,m)=[2a+r(a-r)/s]/(3m)+m[s(5-3m)+3r]/[3(1+m)].
We prove J<=g3. Set A0=2a+r(a-r)/s,K=8-5r. Then
J''(m)=(2/3)[A0/m³-K/(1+m)³]>=0,
because A0/K>=p²/12, m<=2p/(3s)<=3p/4, and
(4+3p)^3-324p=(3p-2)^2(3p+16)>=0.
It suffices to check m0=p/[3(1-p)] and m1=2p/[3(1-r)]. Write y=2p-1,z=r-y. Then 0<=y,z<=1/9. Exact algebra gives
 g3-J(r,m0)=P0/[12(2-y)(1-y)(1+y)(1-y-z)],
 g3-J(r,m1)=P1/[12(1+y)(4-2y-3z)],
P0=y²(y^4-12y^3+46y²-60y+25)+yz(y^4-18y^3+100y²-126y+43)+z²(-6y^3+58y²-58y+22),
P1=y²(2y²-20y+50)+yz(y²-82y+97)+z²(-3y²-102y+45-36z).
Every bracket is positive on [0,1/9]^2 by dropping positive terms and substituting 1/9 in negative ones. Both denominators are positive. Thus J<=g3 and the far case is proved.
