"""Finite-step matrix-weight test infrastructure (numerical evaluation).
For N unit cells [0,N), weights W_i, and W=Id outside, grid_characteristic
computes M over all integer-ended subintervals of [-N,2N]. Analytically
[W]_Ap <= 6**p M: round intervals meeting >=3 cells outward (cost <=3**p);
intervals meeting <=2 cells dominated by uniform adjacent pair (cost 2**p);
truncate outside identity tails to length N (probability domination <=2).
This is a rigorous reduction; floating-point values themselves are not certified.
"""
import numpy as np

def power(A,t):
    d,U=np.linalg.eigh(A)
    assert np.min(d)>0
    return (U*d**t)@U.conj().T

def grid_characteristic(weights,p):
    N=len(weights); mats=[np.eye(2)]*N+list(weights)+[np.eye(2)]*N
    B=[power(W,1/p) for W in mats]; C=[power(W,-1/p) for W in mats]
    q=p/(p-1)
    K=np.array([[np.linalg.norm(a@b,2)**q for b in C] for a in B])
    best=0.; loc=None
    for a in range(3*N):
        for b in range(a+1,3*N+1):
            val=np.mean(np.mean(K[a:b,a:b],axis=1)**(p-1))
            if val>best: best,loc=val,(a-N,b-N)
    return best,loc

def hilbert_average_matrix(N):
    def F(t): return t*np.log(abs(t))-t if t else 0.
    return np.array([[0. if i==j else
       (F(i-j+1)-2*F(i-j)+F(i-j-1))/np.pi
       for j in range(N)] for i in range(N)])

def hilbert_L2_lower(weights):
    N=len(weights); h=hilbert_average_matrix(N)
    block=np.zeros((2*N,2*N))
    for i in range(N):
        for j in range(N):
            block[2*i:2*i+2,2*j:2*j+2]=h[i,j]*power(weights[i],.5)@power(weights[j],-.5)
    return np.linalg.norm(block,2)
