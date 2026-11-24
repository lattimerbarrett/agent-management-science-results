For all restart lengths $s$, the even and odd monic residual polynomials converge with finite total variation. Let $p=p_k,q=p_{k+1},r=p_{k+2}$ and $h=h_k,h'=h_{k+1}$, and put $e=pq-h$. Orthogonality yields $E_w[p f]=0$ and $E_w[p^2qf]=0$ for $\deg f<s$. Also $w''=p^2q^2w/(hh')$. Thus
$$E_{w''}[(r-p)f]=-E_{w''}[pf]=-\frac1{hh'}E_w[e^2pf].$$
The terms linear in $e$ cancel exactly. Since $E_w[e^2]=h(h'-h)$, and $p$ is uniformly bounded in coefficient norm, the right side is $O(h'-h)$ uniformly for $f=1,x,\ldots,x^{s-1}$. The Gram matrices on the orbit closure are uniformly positive definite: otherwise a cluster measure would have at most $s-1$ support points, whereas even support at most $s$ is impossible since a monic degree-$s$ polynomial annihilating that support would force $h_k\to0$, contradicting $h_k\ge h_0>0$. Inverting the Gram matrix for $w''$ gives
$$\|p_{k+2}-p_k\|_{\rm coeff}\le C(h_{k+1}-h_k).$$
Summing proves finite variation for both parity subsequences, and the sharper tail bound $\|p_k-p_{\infty,k\bmod2}\|\le C(h_\infty-h_k)$.

Uniform boundedness of the coefficients of $p$ follows either from compactness and uniform Gram invertibility or from all roots of the orthogonal polynomial lying in the spectral interval. The proof applies unchanged once the distinct active eigenvalues have been chosen.
