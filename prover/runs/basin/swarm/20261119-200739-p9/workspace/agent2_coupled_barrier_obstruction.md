# Exact obstruction to the weighted-minimum ratio barrier

Assume p>2, q=p/(p-1), beta=1/(p-1), L=log Q, and delta=mu_D-1/(2q)>=0. Let
Z_t=B_t+t/(2q), V_t=Z_t+delta*t,
X_t=L-(sup_{s<=t}V_s-V_t), until X hits zero.
Put R_t=exp(-Z_t/q) and m_t=inf_{s<=t}(R_s exp(-beta X_s)).
For each new maximum time of Z, V is also at a new maximum, so X=L. Since X<=L always,
sup_{s<=t}(Z_s+q beta X_s)=sup_{s<=t}Z_s+q beta L.
Consequently the stopping condition R_t=Q m_t is EXACTLY
sup_{s<=t}Z_s-Z_t=q(1-beta)L.
The drawdown of V is no greater than the drawdown of Z (because delta>=0), and q(1-beta)=1-beta^2<1. Thus D=e^X has not hit1 when this weighted ratio stop occurs.

The drawdown U_t=sup Z-Z is reflected Brownian motion with drift -mu_R, mu_R=1/(2q). Its expected hitting time of b is
E_0 tau_b=(exp(2mu_R b)-1-2mu_R b)/(2mu_R^2).
This follows by checking the ODE .5f''-mu_R f'=-1, f'(0)=0, f(b)=0, where
f(u)=(exp(2mu_R b)-exp(2mu_R u))/(2mu_R^2)+(u-b)/mu_R.
For b=q(1-beta)logQ, E tau_b=O_p(Q^(1-beta)). Since D<=Q,
E int_0^tau D_t^alpha dt<=C_p Q^(1+alpha-beta).
This is smaller than the proposed Q^(1+alpha-2epsilon^2) whenever 2epsilon^2<beta. Hence this barrier cannot deliver the desired general-p sharp exponent.

The deterministic supremum identity was also checked on1000 simulated paths, with zero numerical error; see agent2_coupled_barrier_check.py. This is an obstruction to one construction, not a statement about the exact beta(p).
