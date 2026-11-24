# Degree 2 and dense-degree reductions
For a d-regular graph, commute time is dn R_uv.
If d=2 the connected graph is C_n, whose resistance diameter is floor(n^2/4)/n. Thus commute diameter <=n^2/2.
If d>=n/2, let H be the complement. For every x perpendicular to 1,
x^T L_G x=n||x||^2-x^T L_H x >=(2d-n+2)||x||^2,
since x^T L_H x=sum_edges(x_i-x_j)^2<=2(n-1-d)||x||^2.
Consequently R_uv <=2/(2d-n+2), and
dR_uv<=2d/(2d-n+2)<=n/2, where the last inequality is exactly
(n-2)(2d-n)>=0. Again commute diameter <=n^2/2.
All proposed targets exceed n^2/2 on the stated domains. Even n=2mod4 target difference is n(4n-27)/4; even n=0mod4 is n(4n-33)/4. These are positive for n>=10. [CORRECTION: differences actually n(4n-27)/4? target 3n(2n-9)/4 -n^2/2 =n(4n-27)/4, yes.] Odd difference is n(n/2-c) with c at most278/45<15/2. Thus degree2 and d>=n/2 are rigorously excluded from sharpness and satisfy the required bounds.
