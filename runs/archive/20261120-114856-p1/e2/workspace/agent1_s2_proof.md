# Universal convergence for s=2 (draft for independent review)
First discard a finite initial part of the orbit after its last spectral-coordinate annihilation (there are only finitely many eigenvalues, so only finitely many such events). Use the remaining distinct active eigenvalues $\lambda_i$ and squared normalized spectral coefficients $w_i>0$. Let $p_k$ be the monic degree-two orthogonal polynomial for $w_k$, and $h_k=E_{w_k}p_k^2$. Then $w_{k+1,i}=w_{k,i}p_k(\lambda_i)^2/h_k$. Nontermination implies at least three active nodes and $h_k>0$. The usual Cauchy identity is
$$E_{w_k}(p_kp_{k+1}-h_k)^2=h_k(h_{k+1}-h_k).$$
Thus $h_k\uparrow h>0$. Gram matrices are uniformly nonsingular on the orbit closure, because a cluster measure on at most two nodes would imply $h_k\to0$ by testing a monic quadratic annihilating those nodes.

## Polynomial convergence
Put $p=p_k,q=p_{k+1},r=p_{k+2}$ and $e=pq-h_k$. For every linear $f$,
$$E_{w_{k+2}}[(r-p)f]=-E_{w_k}[e^2pf]/(h_kh_{k+1}).$$
Indeed $E[p f]=E[p^2qf]=0$, so the linear terms in $e$ cancel. Uniformly bounded Gram inverses give $\|p_{k+2}-p_k\|\le C(h_{k+1}-h_k)$. Consequently $p_{2k}\to p$, $p_{2k+1}\to q$ with coefficient errors bounded by $C(h-h_{2k})$. Let $P=pq$.

Every cluster measure of the even orbit is supported on $J=\{i:P(\lambda_i)=h\}$. This follows from the displayed Cauchy identity. Also $|P(\lambda_i)|\le h$ for every initially active node: a strictly larger absolute value would eventually multiply its positive weight by a factor greater than one in every double step. For $|P(\lambda_i)|<h$, the weight decays exponentially. If $P(\lambda_i)=-h$, its weight tends to zero (indeed is summable by the Cauchy identity). Since $P-h$ is monic quartic, $|J|\le4$, and $|J|\ge3$ by the positive limiting norm.

All cluster weights on $J$ satisfy $\sum w_i=1$, $\sum w_i p(\lambda_i)=\sum w_i\lambda_i p(\lambda_i)=0$. If $|J|=3$, these equations have a unique solution: $p(\lambda_i)\ne0$ and $1/p(\lambda_i)=q(\lambda_i)/h$ is not the evaluation of a linear polynomial on three nodes (since $q$ is monic quadratic). Thus the coefficient matrix has rank three. Hence the even weights converge.

Suppose $|J|=4$, ordered $a_1<a_2<a_3<a_4$. The same three equations define an affine line, since a polynomial $A+(B+Cx)p(x)$ of degree at most three cannot vanish at four distinct nodes unless identically zero. Intersecting with the simplex gives a compact segment $C$. Every even cluster point lies in $C$. At every point of $C$, the monic orthogonal polynomials are $p,q$ and the double-step map $G=T_2^2$ is the identity; orthogonality of $q$ for the next measure follows from $pq=h$ on $J$. Segment endpoints have at most three nonzero weights.

## Excluding a full-four cluster point when a negative-neutral node is present
Suppose $\xi\notin J$ is initially active and $P(\xi)=-h$. Let $L_i(x)$ be cubic Lagrange basis polynomials at $a_i$. With even indices $k$, set $E_k=h-h_k$, $a_k=\sqrt{h_kh_{k+1}}$, and $\delta P_k=p_kp_{k+1}-P$. Uniformly $\delta P_k=O(E_k)$ in coefficient norm. Define
$$H_k=\log w_{k,\xi}+\sum_{i=1}^4 L_i(\xi)\log w_{k,i}.$$
The double-step weight formula gives, uniformly even if some core weights are tiny,
$$H_{k+2}-H_k=\frac4h(h-a_k)+O(E_k^2).$$
Here the terms in $\delta P_k$ cancel exactly because $\deg\delta P_k\le3$ and $\sum L_i=1$. Moreover $h-a_k\ge E_k/2$. Unless the iteration is already a two-cycle, this increment is positive for all sufficiently large $k$. A full-four cluster point would have core weights bounded below along a subsequence, whereas $w_{k,\xi}\to0$, forcing $H_k\to-\infty$ along that subsequence, impossible for an eventually increasing sequence. Therefore no full-four cluster point exists. All cluster points are segment endpoints, a finite set. Since $\|w_{k+2}-w_k\|\to0$, the even weights converge.

## The remaining case: exponential approach to the four-node face
If no initially active node has $P=-h$, all outside weights decay exponentially. Let $u_k$ be the normalized restriction of $w_{2k}$ to $J$, and let $F$ be the exact double-step map on that four-node simplex. Then
$$u_{k+1}=F(u_k)+O(\rho^k),\qquad0<\rho<1.$$
The cluster set is contained in $C$.

At each point $c\in C$, $DF(c)=I+N(c)$, where $\operatorname{range}N(c)\subseteq\operatorname{span}V$, $N(c)V=0$, and $V$ is the constant direction of the affine segment. This follows directly from the quadratic polynomial-increment identity: near a point of $C$, the coefficient difference $p(Fw)-p(w)$ is quadratic in $w-c$, since the polynomial defect vanishes on all four nodes at $c$. Thus $Dp(c)(DF(c)-I)=0$. The kernel of $Dp(c)$ in the normalized-weight tangent space is precisely $\operatorname{span}V$, by the rank-three calculation above. Also $DF(c)V=V$, since $F$ fixes $C$. This holds at endpoints by continuity; in the $p=q$ case $N=0$. In a basis whose first vector is $V$, all $N(c)$ have only their first row possibly nonzero, with zero first entry. Rescaling the transverse basis vectors makes $DF$ and its inverse uniformly as close to the identity in operator norm as desired along $C$. Thus for any $L>1$, in a sufficiently small neighborhood of $C$, $F$ has a common inverse branch and $F^{-1}$ is $L$-Lipschitz. More explicitly, choose a small convex tubular neighborhood of the segment on which, in the adapted norm, $\|DF-I\|<\eta<1$. Integrating derivatives along line segments proves injectivity, and the inverse function theorem supplies a common inverse on a smaller convex tube of $C$, with derivative norm at most $(1-\eta)^{-1}$.

Choose $L\rho<1$. Pulling $u_N$ back under $F$ to a late index $K$ gives a Cauchy sequence, since the error at index $j$ is at most $O(\rho^j)$ and its backward propagation is bounded by $L^{j-K}$. The limits produce an exact orbit $v_{k+1}=F(v_k)$ with
$$\|v_k-u_k\|=O(\rho^k).$$
All pullbacks remain in the neighborhood by the geometric-series bound. If the original orbit has a full-four cluster point, choose $K$ arbitrarily late at such an interior visit; then $v_K$ has positive weights because the correction is exponentially small. Thus $v_k$ is a genuine positive four-node orbit, and has the same cluster set as $u_k$. If no full-four cluster point exists, convergence was already proved by the finite-endpoint argument.

## Exact four-node convergence
If the exact shadowing orbit ever annihilates a coordinate, it is thereafter on at most three nodes; its double-step map is the identity, so it already converges. Otherwise interleave $v_{k+1}=F(v_k)$ with the single-step images $T_2(v_k)$ and relabel the resulting full block orbit. For positive weights $v$ on four nodes, put $d_i=1/\prod_{j\ne i}(a_i-a_j)$ and
$$\theta(v)=\frac{\sum a_i d_i^2/v_i}{\sum d_i^2/v_i}.$$
The duality formula gives $T_2(v)_i\propto(d_i^2/v_i)(a_i-\theta(v))^2$. If $a=\theta(v),b=\theta(T_2v),c=\theta(T_2^2v)$ and $z_i\propto d_i^2/v_i$, direct algebra gives
$$c-b=(b-a)\frac{\sum z_i(a_i-a)/(a_i-b)}{\sum z_i((a_i-a)/(a_i-b))^2}.$$
When $a,b$ lie in one spectral gap, the ratio is positive.

If an exact orbit has a full-four cluster point, the limiting monic polynomials $p,q$ each have one root in $(a_1,a_2)$ and one in $(a_3,a_4)$. Indeed $pq=\prod_i(x-a_i)+h$ has its four roots in these two negative wells, and neither orthogonal quadratic can have both roots in a gap without a support node between them. For all sufficiently late blocks, the actual monic orthogonal quadratics have the same root locations. The numerator of the Stieltjes transform of $T_2v$ is the product of that monic quadratic and $x-\theta(v)$. Stieltjes zeros strictly interlace the four nodes, so $\theta(v_k)\in(a_2,a_3)$ for all sufficiently large $k$. The recurrence therefore makes $\theta(v_k)$ monotone, hence convergent. A full-four cluster point forces its limit to lie strictly inside the middle gap. The exact double-step weight formula then bounds changes of all log weight ratios by $C|\theta(v_{k+1})-\theta(v_k)|$, a summable sequence. Hence the even weights converge. If no full-four cluster point exists, they converge by the finite-endpoint argument.

Finally, weight convergence implies convergence of normalized even residuals: on every coordinate whose limiting weight is positive, $p_{2k}(\lambda_i)p_{2k+1}(\lambda_i)\to h>0$, so its even-block sign is eventually constant. Vanishing coordinates do not matter. Eigenspace directions are fixed by the initial residual.
