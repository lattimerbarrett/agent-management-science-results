from scipy.optimize import linprog
# Necessary scalar constraints: t_n=tau(a_n),
# eta <= t_(n+1), and eta <= 1-t_n, since
# a_(n+1)-a_n <= a_(n+1), 1-a_n.
# Maximize eta for several finite lengths.
for N in (2, 3, 10):
    # variables t_0,...,t_N,eta
    rows=[]; rhs=[]
    for n in range(N):
        r=[0.]*(N+2); r[-1]=1; r[n+1]=-1
        rows.append(r); rhs.append(0.)
        r=[0.]*(N+2); r[-1]=1; r[n]=1
        rows.append(r); rhs.append(1.)
        r=[0.]*(N+2); r[n]=1; r[n+1]=-1
        rows.append(r); rhs.append(0.)
    c=[0.]*(N+2); c[-1]=-1
    result=linprog(c,A_ub=rows,b_ub=rhs,bounds=[(0,1)]*(N+2),method='highs')
    print(f'{N} increments: necessary scalar bound eta <= {-result.fun:g}')