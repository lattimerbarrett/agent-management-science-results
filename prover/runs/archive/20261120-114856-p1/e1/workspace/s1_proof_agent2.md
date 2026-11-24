# Completed s=1 proof
Let the distinct eigenvalues present in r_0 be lambda_i, with fixed unit eigenspace directions v_i=E_i r_0/||E_i r_0||. Every normalized residual is a linear combination of these finitely many fixed v_i.
For a unit vector y let mu=y^T A y, delta=A-mu I, sigma^2=y^T delta^2 y. Nontermination implies sigma>0. The steepest descent residual direction is T(y)=-delta y/sigma. Put m_j=y^T delta^j y. Direct expansion gives
mu(Ty)-mu=m_3/m_2,
sigma(Ty)^2-sigma(y)^2=||(delta^2-(m_3/m_2)delta-m_2 I)y||^2/m_2 >=0.
Thus sigma_k increases to L>0. Its equality condition says that the spectral support of y is contained in the roots of a monic quadratic, hence has at most two eigenvalues.
Moreover <y,T^2y>=sigma(y)/sigma(Ty), hence ||T^2y-y||^2=2(1-sigma(y)/sigma(Ty))->0.
The map T is continuous on the compact orbit closure because sigma>=sigma_0>0 there. For any cluster point z, continuity gives sigma(Tz)=sigma(z)=L; consequently z has exactly two eigenvalue components. Write z=a v_i+b v_j. Then a^2+b^2=1 and a^2 b^2(lambda_i-lambda_j)^2=L^2. There are finitely many choices of i,j and finitely many corresponding a,b, including signs. Therefore the cluster set is finite.
Finally any sequence in a compact set with successive differences tending to zero and a finite cluster set converges. Indeed sufficiently late terms lie in disjoint small neighborhoods of the finitely many cluster points, and sufficiently small steps prevent switching neighborhoods. Apply this to y_{2k}.
Exact symbolic and rational checks: workspace/s1_checks_agent2.py (ran successfully).
