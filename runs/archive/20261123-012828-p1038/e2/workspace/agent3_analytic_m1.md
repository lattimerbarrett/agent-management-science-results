# Elementary analytic proof that the displayed formulas imply 1 in S

All parameters in this note concern m=1. Set ring heights h_-=0,h_+=1/10, radii r=1,R=100. Initially allow a=b=k lower axial points to coalesce at L=-30 and upper axial points at U=3/5; these are well-defined polynomial limits when points split along the axis.

Put rho(d,c)=c/(d+sqrt(d^2+c^2)) and
x=rho(30,1), y=rho(301/10,100), u=rho(3/5,1), v=rho(1/2,100), q=rho(1/10,99).
Direct substitution into the displayed factors gives ring polynomials
A(T)=G_A(T)^k(1-qT), B(T)=G_B(T)^k(T+q),
where G_A(T)=(T+x)(1+uT), G_B(T)=(T+y)(1+vT).
The lower axis rows are T^j(1-xT)(1-yT), 0<=j<k; the upper rows are T^{k+j}(T-u)(T-v), 0<=j<k.
Moving the upper rows before A,B incurs sign (-1)^(2k)=1.

## Dual kernels and orientation
For s=u,v define a length-(2k+2) vector K_s by
K_s(j)=s^(j-k) for j>=k,
K_s(j)=C_s*x^(k-j)+D_s*y^(k-j) for j<=k,
C_s=(s-1/y)/(1/x-1/y), D_s=(1/x-s)/(1/x-1/y).
Both formulas agree at j=k, and the lower formula continued to k+1 equals s. Thus each axis row annihilates K_s. Since 0<x<y<1 and 0<u<v<1, C_s<0, D_s=1-C_s>1, and K_s(j)>0 everywhere. Moreover
0<K_s(j)<=D_s*s^(j-k) for all j.
Indeed for j<k, K_s(j)<=D_s*y^(k-j)<=D_s*s^(j-k), since ys<1.

Let A_s=sum_j A_j K_s(j), B_s=sum_j B_j K_s(j). The full matrix determinant has the same sign as
E_k=A_u B_v-A_v B_u.
To verify orientation: for canonical annihilator columns W0,W1 with initial values (1,0),(0,1), respectively, det M=(xy)^k det(pairings with W0,W1), as follows by the determinant-one column transformation [e_2,...,e_(2k+1),W0,W1]. At indices k,k+1, the columns K_u,K_v have matrix [[1,1],[u,v]] with positive determinant v-u. The transfer matrices for the lower recurrence have positive determinant 1/(xy), so the initial 2x2 determinant of K_u,K_v is also positive. Hence switching from W columns to K columns preserves sign.

## Elementary exponential bounds
Define g_A(t)=G_A(t)/t and g_B(t)=G_B(t)/t, and tau_A=sqrt(x/u), tau_B=sqrt(y/v).
All constants below are fixed and independent of k.

1. Coefficientwise |A_j| is bounded by the coefficient of (1+qT)G_A(T)^k. The kernel bound therefore gives
|A_u| <= D_u(1+qu) g_A(u)^k.
Since every coefficient of B is positive, likewise
0<B_v <= D_v(v+q) g_B(v)^k.
Thus A_u B_v <= C [g_A(u)g_B(v)]^k.

2. Since K_v(j)=v^(j-k) for j>=k,
A_v=v^(-k)A(v)+sum_(j<k) A_j[K_v(j)-v^(j-k)].
The absolute value of the correction is at most
(D_v+1) sum_(j<k) |A_j|v^(j-k)
<= (D_v+1)(1+q tau_A)g_A(tau_A)^k,
because v>tau_A and j-k<0. As g_A(t)=ut+1+xu+x/t has its strict minimum at tau_A, g_A(tau_A)<g_A(v). Since qv<1, eventually
A_v >= (1-qv)/2 * g_A(v)^k >0.

3. K_u(k)=1 and B has positive coefficients, so
B_u>=B_k>=q[T^k]G_B(T)^k.
Let a=sqrt(yv). Then G_B(tau_B z)/tau_B=H(z)=a+(1+a^2)z+az^2.
Its kth power has maximal coefficient at degree k. One elementary proof is
H(z)^k=sum_(j=0)^k binom(k,j)a^j(1-a)^(2(k-j)) z^(k-j)(1+z)^(2j);
every summand has its maximal coefficient at degree k by the central-binomial inequality. Therefore
[T^k]G_B(T)^k=[z^k]H(z)^k >= H(1)^k/(2k+1)=g_B(tau_B)^k/(2k+1).
Consequently A_v B_u >= c [g_A(v)g_B(tau_B)]^k/(2k+1) for all sufficiently large k, with c>0.

Combining these estimates,
E_k <= C [g_A(u)g_B(v)]^k - c [g_A(v)g_B(tau_B)]^k/(2k+1).

## All scalar inequalities have simple rational bounds
Squaring positive rational bounds in the definitions of rho gives
83/5000 < x < 167/10000,
743/1000 < y < 93/125,
283/500 < u < 567/1000,
199/200 < v < 249/250,
499/500 < q < 999/1000.
These imply tau_A<u<tau_B<v and qv<1.
Also, directly from g_A(t)=ut+1+xu+x/t and g_B(t)=vt+1+yv+y/t,
g_A(u)g_B(v)
 < ((567/1000)^2+1+(167/10000)(567/1000)+(167/10000)/(283/500))
   *((249/250)^2+1+(93/125)(249/250)+(93/125)/(199/200))
 < 19/4 = 4.75.
On the other hand,
g_A(v)> (283/500)(199/200)+1+(83/5000)(283/500)+(83/5000)/(249/250)> 158/100,
and sqrt(yv)>85/100, so
g_B(tau_B)=(1+sqrt(yv))^2 > (185/100)^2.
Thus g_A(v)g_B(tau_B)>(158/100)(185/100)^2>54/10=5.4.
It follows that E_k<0 for every sufficiently large k.

## Restoring distinct points and obtaining singularities
For each sufficiently large k, split the lower heights as -30+j epsilon and upper heights as 3/5+j epsilon, 0<=j<k. Polynomial coefficients depend continuously on these axial heights even at this clustered limit (axis-axis factors remain exactly 1 or T). Hence for a sufficiently small epsilon>0 the actual distinct admissible configuration still has det M<0.
Fix these distinct heights and scale both radii by t>0, replacing (1,100) with (t,100t). All coefficients are real and continuous in t. As t decreases to zero, all points approach distinct points of the vertical axis, and row i tends to T^(i-1). Therefore det M tends to 1. The intermediate value theorem gives a singular admissible configuration for some 0<t<1.
This construction works for every sufficiently large k and n=2k+2 is unbounded. Thus the literal displayed definitions imply 1 in S, contradicting the requested S={m>=3}.
