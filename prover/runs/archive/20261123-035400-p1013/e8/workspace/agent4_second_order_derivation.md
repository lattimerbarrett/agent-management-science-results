# Second-order comparison for r=4
## Cross-part cycles
Let s_i=n_i-n/4, sum s_i=0, bounded; S_j=sum s_i^j.
Write c_cross(n_1,...,n_4) for all cycles in the complete 4-partite graph.
A multivariate Perron saddle computation yields

log c_cross = log K_n - 2 S_2/n + [(41/6) S_2-(16/3)S_3]/n^2+o(n^-2),
K_n=C Gamma(n)(3/4)^n[1-5/(12n)+O(n^-2)].

The computation itself is exactly reproduced by agent4_edgeworth.py; a full proof also needs uniform control of Taylor-integral remainder (standard analytic saddle argument, not encoded as assertions).

Details: for weighted proper cyclic words use matrix A(z) with offdiagonal entry z_j and zero diagonal. Its Perron root lambda satisfies sum z_i/(lambda+z_i)=1. Normalize lambda=1 and put y_i=z_i/(1+z_i). Then sum y_i=1 and stationary proportions p_i=y_i(1-y_i)/sum y_j(1-y_j). The contrast covariance is
V=[diag(a b)-(a b)p^T-p(a b)^T+(sum a b)pp^T]/sum a,
where a_i=y_i(1-y_i), b_i=1-2y_i.

At p_i=1/4, eigenvalue on contrasts is1/8. Legendre entropy plus factorial entropy has expansion -2 sum epsilon_i^2 -(16/3)sum epsilon_i^3. The square-root factorial/saddle prefactor gives coefficient B_H=3/2. Omitting vertices to count all cycles multiplies Hamilton cycles by exp(sum z_i)[1+O(1/n)]. Expanding sum z_i at balance adds16/3 to B, giving41/6.

For K_n's1/n coefficient, put v_i=t_i-mean(t), S_j=sum v_i^j. The compact derivative table is log lambda(e^t)=log3+mean(t)+S_2/16-S_3/192-5S_4/768+S_2^2/512+O(||v||^5). Under the contrast Gaussian with covariance8(I-J/4), E S_4=432, E S_2^2=960, E S_3^2=4608. Thus the word correction is -5*432/768+960/512-4608/(2*192^2)=-1. Equivalently expand log lambda(e^t) with t_4=0 through degree4. If its homogeneous degree j part is L_j, and X Gaussian with inverse covariance Hess(L_2)^-1 (diagonal16, offdiagonal8), the local word coefficient is E[L_4(X)-L_3(X)^2/2]=-1. Stirling contributes(4^2-1)/12=5/4, so Hamilton kappa=1/4. Poisson vertex omissions contribute Lambda-A=4/3-2=-2/3, hence total kappa=-5/12.

## Internal forests and mandatory supervertices
For a selected internal linear forest with e edges and p nontrivial path components, contract each path; multiply by2^p and require the p supervertices to appear in the cross cycle. Inclusion-exclusion handles this requirement.
Set D=4/3, R=D/n, A=2, B=41/6, C=-16/3, kappa=-5/12.
For offsets s, put s'_i=s_i-e(1_{i=1}-1/4), S'_j=sum (s'_i)^j.
L_1(e)=e(e+1)/2-A S'_2,
L_2(e)=e(e+1)(2e+1)/12+kappa e-A e S'_2+B S'_2+C S'_3.
The ratio of cross-cycle counts with e contractions and p mandatory vertices to K_n is
R^e[1+P_1(e,p)/n+P_2(e,p)/n^2+o(n^-2)],
where
P_1=L_1(e)-pD,
P_2=L_2(e)+L_1(e)^2/2-pD L_1(e+1)+p(p-1)D^2/2.

For each fixed component, let a_j(w) be its selected j-edge linear-forest polynomial weighted2^{pathcomponents} w^{pathcomponents}. Its logarithmic generating polynomial through cubic order is
 a_1(w)x+[a_2(w)-a_1(w)^2/2]x^2+[a_3(w)-a_1(w)a_2(w)+a_1(w)^3/3]x^3.
For d-edge star: a_1=2dw, a_2=2 binom(d,2)w,a_3=0.
For d-edge path: a_j=sum_{p=1}^{min(j,d-j+1)}binom(j-1,p-1)binom(d-j+1,p)2^p w^p.

## Exact symbolic result
n=32q+10. Star host has parts(8q+3,8q+3,8q+2,8q+2), internal(q-1)K_{1,7} union K_{1,10}.
Path host has parts(8q+4,8q+2,8q+2,8q+2), internal qP_8 union P_4.
Both have7q+3 internal edges; the star host has exactly one more edge overall.
The leading forest selection distribution has e=p=Poisson(7/12). Sum the displayed P_1,P_2 against this distribution, including first/second corrections from the component generating polynomials (agent4_second_order.py does exact rational polynomial algebra).

c_star/(K_n exp(7/12))=1-51/(16n)-69155/(4608n^2)+o(n^-2),
c_path/(K_n exp(7/12))=1-51/(16n)+181655/(13824n^2)+o(n^-2).
Hence c_path/c_star=1+760/(27n^2)+o(n^-2)>1 for all sufficiently large q.

This completes the analytic coefficient calculation but DOES NOT by itself establish that the star host is edge-extremal for any fixed H; the realization + global structural reduction are separate requirements.
