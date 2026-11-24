# Greedy mixed lemma: full proof (agent 3)

Assume graphon book bounds a,b with 0<a<=b<1/2 and sqrt(a)+sqrt(b)<1. Twin arguments give R red-clique of mass s<=a, B remaining beta=1-s; R rows have red L2 <=a, B rows blue L2 <=b. B-support is K4-free: a B-K4 and clique quadratic force random bound once a>=1/16; global B-triangle/tangent forces a>1/12, so this applies. Alternatively obtain a>1/12 after the greedy selection below (K4-freeness for a<1/16 can first follow an unrestricted K4 lambda=2 giving b+3a>=3/4, impossible b<1/2,a<1/16).

**Greedy selection.** Put h(v)=int_R W(v,r)^2 dr. Choose minimum-h B vertex, remove its support nonneighbors A1; then minimum-h vertex in remaining common neighborhood, remove its nonneighbors A2, etc. Essential infima / epsilon minimizers and a limit suffice. K4-free implies termination k<=3. Every page in Ai has gi=0 and h(vi)<=h(page), hence sum_i xi hi<=int_B h<=s(a-s), with xi=|Ai|, hi=h(vi). All selected pairs have red support and hence their red Gram <=a. Roots are B, so blue row norms<=b.

k=1 contradicts b>=beta>3/4. For k=2, each xi<=b and therefore xi>=beta-b. Put H=h1+h2 and m=int_R(g1+g2). Then H<=s(a-s)/(beta-b), m<=sqrt(2sH), and 2b>=beta+int_R[(1-g1)^2+(1-g2)^2]=1+s-2m+H. Let q^2=(a-s)/(2(beta-b))<=a=u^2<1/4. Since H<=2sq^2<2s and the displayed expression decreases with H, 2b>=1+s(1-4q+2q^2)>=1+s(1-4u+2u^2). If u<=1-1/sqrt2 this gives b>=1/2. Otherwise s<=a gives b>=1/2+a(1/2+a-2u)>=(1-u)^2, since difference equals (u^2-1)(2u^2-4u+1)/2>=0 for 1-1/sqrt2<=u<=1/2. Contradiction. Thus k=3.

## Main finite inequality
Write gi=root red rows, xi=|Ai|, and hi=int_R gi^2. Let Mij=int_R gi gj, L_R=int_R sum_i(1-gi)^2. For any ell_i in [0,2], on Ai the coordinate gi vanishes, so
sum_j(1-gj)^2 + sum_i ell_i gj gk >= 3-4/(2+ell_i),
where {i,j,k}={1,2,3}. This follows by completing the two-variable square. Thus for any K,kappa>0 such that ell_i=4/(3-K+kappa hi)-2 lies in [0,2],
3b+a sum_i ell_i >= beta K - kappa sum_i xi hi + L_R + sum_i ell_i Mjk
>= beta K - kappa s(a-s) + L_R + sum_i ell_i Mjk. (1)

First take u=sqrt(a), u in [1/sqrt12,q*], q*=4/sqrt3-2. Put
ell=2/(sqrt3 u)-2, t=2sqrt3 u, K=3-t,
kappa=3-(2sqrt3-3)/u.
Then sqrt3<=ell<=2, 0<kappa<=3/2, and a<12/125. Since hi<=s<=a, denominators t+kappa hi are between1 and2, so ell_i in[0,2]. Define D to be the resulting lower bound for 3b minus (K-3a ell):
D=beta K-kappa s(a-s)+L_R+sum ell_i Mjk -a sum ell_i -(K-3a ell).
We show D>=0. If s=0 this is immediate. Otherwise let E denote expectation on R, r_i=gi|R, H_i=E r_i^2, N_jk=E r_j r_k, Q=sum H_i, S=E sum r_i. Put zeta=kappa s/t. Since
ell-ell_i=kappa s H_i/[3a(1+zeta H_i)],
exact rearrangement gives
D/s=E F0(r)+kappa s
 -(kappa zeta/3)sum H_i^2/(1+zeta H_i)
 -(kappa s/(3a))sum H_i N_jk/(1+zeta H_i),
where F0(r)=sum(1-r_i)^2+ell sum_pairs r_i r_j+kappa sum r_i^2/3-kappa a-K.
Cauchy N_jk<=sqrt(H_j H_k) and AMGM imply sum H_i N_jk<=Q^2/3; also sum H_i^2<=Q^2. Consequently
D/s>=E F0+kappa s(1-C Q^2), C=kappa/(3t)+1/(9a)<=11/6. (2)
The AMGM claim follows by writing H_i=z_i^2: product(z_i)sum(z_i)<= (sum z_i^2)^2/3; this is Schur/Muirhead (expand the difference into known nonnegative symmetric quartic).

The exact completion is
F0=(sum r_i-3u)^2/(3u)+c(u)[sum r_i^2-(sum r_i)^2/3]+3u(q*-u),
c(u)=3-(sqrt3-1)/u>=cmin=2sqrt3-3>0.
Thus E F0>=0. Also using S>=Q (r_i in[0,1]), Jensen, ell>=sqrt3, and
3-K-kappa a=(4sqrt3-3)u-3u^2>=Cmin=7/4-sqrt3/2,
we have
E F0>=Cmin-2S+cmin Q+(sqrt3/2)S^2. (3)
If Q<=sqrt(6/11), (2) is nonnegative. Otherwise use kappa s<=18/125, minimize(3) over S>=Q, and subtract (18/125)((11/6)Q^2-1). For Q between sqrt(6/11) and2/sqrt3 the resulting function is concave quadratic in Q, positive at both endpoints. For Q>=2/sqrt3 it is a quadratic with positive leading coefficient and NEGATIVE discriminant. All endpoint signs and discriminants are checked EXACTLY by workspace/agent3_greedy_certificate.py. Hence D>=0 and
3b>=K-3a ell=3+6a-4sqrt(3a), proving b>=1+2a-4sqrt(a/3).

## Random side a in [a*,1/9]
Here a*=q*^2. Freeze ell=sqrt3, t=4/(2+sqrt3), K=4sqrt3-5, kappa=3/2 at the previous endpoint. Choose the same ell_i=4/(t+kappa hi)-2. Again [0,2] range holds. For frozen parameters, write delta_i=ell-ell_i. The positive term (a/s)sum delta_i in D/s is at least (a*/s)sum delta_i because a>=a*. Apply this lower bound, recovering the same kappa Q/3 baseline as at a*. The negative delta_i N_jk term uses t^2=12a*, so now C=kappa/(3t)+1/(9a*)<5/3 (exact check). The baseline F0 at a equals its nonnegative endpoint version minus kappa(a-a*). Thus use E F0+kappa(a-a*) in(2)-(3), with kappa s<=1/6. The same two-polynomial check is positive (certificate script). Therefore D/s>=-kappa(a-a*), and
b>=K/3-sqrt3 a-(a/2)(a-a*).
This exceeds or equals (1-sqrt a)^2 for a in[a*,1/9]. Set u=sqrt a: difference is concave quartic (second derivative negative), zero at q*, positive at1/3, so nonnegative throughout. Exact checks in script. This contradicts above-random assumption.

For a>=1/9 the unrestricted Btriangle clique quadratic directly gives b>=(1-sqrt a)^2 (optimizer ell=1/sqrt a-1<=2). Thus no above-random feasible graphon has a>=a*.
