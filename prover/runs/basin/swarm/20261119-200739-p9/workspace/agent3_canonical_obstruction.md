# Obstruction for the asymmetric canonical-pair model

Let p>2, q=p/(p-1), and let a,c be positive terminal random variables with E_P a=1. Set dmu=a dP, R=c/a, and let

M=[[a^(1/p), a^(1/p) h],[0,a^(1/p)/c]].

Direct triangular inversion shows the off-diagonal entry of M(x)M(y)^(-1) equals a(x)^(1/p)c(y)a(y)^(-1/p)(h(x)-h(y)). Consequently the characteristic is at least

C=E_mu,x (E_mu,y R(y)^q |h(x)-h(y)|^q)^(p/q).

Suppose E_mu[R^q h]=0, e.g. the stopping rule depends only on B1, R depends only on B1, and h is a centered Gaussian conditional on B1 (driven by an independent B2).
Writing Z=E_mu R^q, weighted Jensen gives
E_mu,y R(y)^q |h(x)-h(y)|^q >= Z |h(x)|^q.
Therefore

C >= Z^(p/q) E_mu |h|^p.

Thus the dual-ratio penalty and primal angular moment multiply in the actual characteristic. They cannot be removed merely by improving a triangle-inequality estimate.

Gaussian centering is not essential. For general h with E_mu h=0, write b=E_mu[R^q h]/Z. Weighted Jensen yields C>=Z^(p/q) E_mu|h-b|^p. Since |b|<=||h-b||_p and ||h||_p<=2||h-b||_p, one has the universal bound C>=2^(-p) Z^(p/q) E_mu|h|^p. Thus common-noise correlation cannot erase this product cost in a closed canonical martingale pair.

A further Ito obstruction: for scalar stretch noises da=a sa dB1, dc=c sc dB1 and dh=u dB1+v dB2+b dt, requiring both ah and ch to be martingales forces b=-sa u=-sc u. Hence when sa!=sc one must have u=b=0. In higher noise dimension the necessary condition is (sa-sc).eta=0 and drift_h=-sa.eta.
