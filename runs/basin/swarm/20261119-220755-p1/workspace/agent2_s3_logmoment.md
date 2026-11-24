# Exact s=3, five-base-node logarithmic moment
Let P(x)=prod_{i=1}^5(x-lambda_i), fg-L=P Q with Q=x-c, and let mu!=nu satisfy fg(mu)=fg(nu)=-L.
Define
 a=Q(mu)/(mu-nu), b=-Q(nu)/(mu-nu),
 c_i=2L/[P'(lambda_i)(lambda_i-mu)(lambda_i-nu)].
Then a+b=sum_i c_i=1. For every monic sextic K,
 sum_i c_i K(lambda_i)-a K(mu)-b K(nu)=2L.
Indeed these are 2L times the seven-node barycentric weights: for mu, P(mu)=-2L/Q(mu), and similarly nu. The leading coefficient interpolation formula proves the identity.

For any exact restarted residual orbit with limiting even/odd cubics f,g, L=N_infty>0 and these five positive-level and two negative-level nodes active, put
 Psi_k=sum_i c_i log p_{k,i}+a log p_{k,mu}+b log p_{k,nu}.
Write K_k=f_k f_{k+1} and R_k=sqrt(N_k N_{k+1}), t_k=L-N_k. Polynomial total variation gives K_k-fg=O(t_k). Exact two-block residual update and Taylor expansion imply
 Psi_{k+2}-Psi_k=4 log(L/R_k)+O(t_k^2).
The linear Taylor terms vanish by the sextic interpolation identity, since K_k-fg has degree <=5. Thus unless the orbit is eventually a two-cycle, this difference is >= c t_k eventually. Any active negative-level mode forces sum t_k=infinity, since otherwise its log weight has summable increments and cannot tend to zero. Hence Psi_k -> +infinity along each parity. Crucially, this calculation requires no positive lower bound on the five base weights.

## Continuous blowup identity
Use H=x-theta, physical scalar A=delta N, and h'=-theta'. Let q=gw+f dg-A. The dual differential gives q(lambda_i)=Lh'/(2H(lambda_i)). Thus
 q(x)=P(x) C + (Lh'/2) [1-P(x)/P(theta)]/(x-theta)
for a scalar C. At a negative mode z,
 ell_z=2(w(z)/f(z)+dg(z)/g(z))-2A/L=-2q(z)/L-4A/L.
The above weighted logarithm, using p_i proportional lambda_i-theta, has derivative
 d/dtau [a log Z_mu+b log Z_nu+Phi(theta)] =2-4A/L,
where
 Phi'(theta)=[Q(theta)+2L/P(theta)]/[(mu-theta)(nu-theta)]
 =R4(theta)/P(theta), R4=(P Q+2L)/[(x-mu)(x-nu)].
Partial fractions give Phi=sum_i c_i log|theta-lambda_i|. In homogeneous time the +2 is absent. Therefore no compact positive recurrent orbit of the logtime ODE with A<0 can exist in this five-base/two-charge stratum.

This does NOT by itself close the s=3 lower bound: boundary charge ratios and theta endpoint excursions still require a no-return estimate.
