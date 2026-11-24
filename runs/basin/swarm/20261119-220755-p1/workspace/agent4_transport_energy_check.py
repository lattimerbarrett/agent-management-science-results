"""Numerical necessary-condition test, NOT a proof of nonexistence of energy."""
import numpy as np,sys
from scipy.integrate import solve_ivp
from scipy.linalg import null_space
sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
D=np.load('workspace/agent2_rational_positive_eq_0.4.npz')
ob=BlowupODE(D['base'],D['f'],D['g'],float(D['N']),D['mus']);s=ob.s;z=len(ob.mus)
def frame(theta):
 base=np.r_[-theta,np.zeros(s+z)]
 b=np.array([-ob(0,base+np.eye(1+s+z)[1+j],False)[0] for j in range(s)])
 j=np.argmax(abs(b));u=np.zeros(s);u[j]=1/b[j]
 K=-ob(0,np.r_[-theta,u,np.zeros(z)],False)[1:1+s]
 F=np.column_stack([ob(0,base+np.eye(1+s+z)[1+s+i],False)[1:1+s] for i in range(z)])
 L=np.column_stack([ob(0,np.r_[-theta,np.eye(s)[j],np.ones(z)],False)[1+s:] for j in range(s)])
 return b,K,F,L
th0=.64
rhs=lambda t,u:(-np.outer(frame(t)[1],frame(t)[0])@u.reshape(s,s)).ravel()
solp=solve_ivp(rhs,[th0,.98],np.eye(s).ravel(),rtol=1e-10,atol=1e-11,dense_output=True)
solm=solve_ivp(rhs,[th0,.02],np.eye(s).ravel(),rtol=1e-10,atol=1e-11,dense_output=True)
inds=[(i,j) for i in range(s) for j in range(i,s)]
Gs=[]
for i,j in inds:
 G=np.zeros((s,s));G[i,j]=G[j,i]=1;Gs.append(G)
A=[]
for theta in np.linspace(.05,.95,19):
 U=(solp if theta>th0 else solm).sol(theta).reshape(s,s)
 b,K,F,L=frame(theta);B=b@U;FF=np.linalg.solve(U,F);LL=L@U
 for j in range(z):
  perp=null_space(np.array([B,LL[j]]))
  A.extend(np.column_stack([perp.T@G@FF[:,j] for G in Gs])/np.linalg.norm(FF[:,j]))
A=np.array(A);us,ss,vs=np.linalg.svd(A,full_matrices=False)
print('necessary-condition singular values',ss)
G=sum(c*g for c,g in zip(vs[-1],Gs))
print('apparent null metric eigenvalues',np.linalg.eigvalsh(G))
for theta in [.1,.3,.64,.8,.95]:
 U=(solp if theta>th0 else solm).sol(theta).reshape(s,s)
 b,K,F,L=frame(theta);B=b@U;FF=np.linalg.solve(U,F);LL=L@U
 for j in range(z):
  cc=np.linalg.lstsq(np.array([LL[j],B]).T,-G@FF[:,j],rcond=None)[0]
  print('theta, charge, implied c and dc/dtheta',theta,j,cc)
