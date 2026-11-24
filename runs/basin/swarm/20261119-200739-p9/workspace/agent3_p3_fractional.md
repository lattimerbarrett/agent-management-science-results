# Exact fractional-endpoint formula at p=3

Let M be constant M_i on finitely many intervals of arbitrary positive lengths, and put K_ij=||M_i M_j^(-1)||^(3/2). For any test interval, if l_i is its overlap length with cell i, the characteristic contribution is exactly

A_I = sum_i l_i (sum_j l_j K_ij)^2 / (sum_i l_i)^3.

Fix the first and last intersected cells. Their lengths u,v are variable; all interior cells are fully present. Let L0 be the sum of interior lengths, a,b the available endpoint-cell lengths, and mu the interior-cell probability vector. If L0>0, put x=u/(L0+u+v), y=v/(L0+u+v), z=(1-x-y,x,y). The feasible (x,y) region is the quadrilateral with vertices

(0,0), (a/(L0+a),0), (a/(L0+a+b),b/(L0+a+b)), (0,b/(L0+b)).

For each row i let V_i=(sum_internal mu_j K_ij, K_i,left, K_i,right). Define
Q0=sum_internal mu_i V_i V_i^T,
Q1=V_left V_left^T,
Q2=V_right V_right^T.
Then A_I = z0 z^T Q0 z + z1 z^T Q1 z + z2 z^T Q2 z, an explicit cubic polynomial in x,y.

Consequently its maximum is found among the four vertices, zeros of the quadratic derivative on each edge, and interior zeros of two quadratic partial derivatives. The latter reduce to a quartic resultant. Degenerate critical curves require limiting or separate handling, but do not create an algorithmic infinite-dimensional problem. For adjacent cells L0=0, every mixture of the two endpoint values is feasible and one maximizes a univariate cubic on [0,1]. A one-cell interval has characteristic 1.

Code agent3_p3_fractional.py implements the generic stationary/edge enumeration with floating arithmetic. It was checked against an independent global optimizer on 100 random cases with 3--7 root matrices and cell length ratios up to exp(6), relative discrepancy below 6.1e-10. These are genuine numeric checks, not a claim of interval-arithmetic certification.

At p=2 the identical normalization yields a quadratic polynomial, so interior stationary equations are linear and edge derivatives linear. At p=m+1 for integer m>=1 the numerator has degree m+1, with coefficients involving fixed kernel powers q=(m+1)/m; fixed-endpoint normalized characteristic is a polynomial of degree m+1 on the same quadrilateral.
