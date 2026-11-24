import sys, numpy as np
sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
from scipy.integrate import solve_ivp
D=np.load('workspace/agent2_rational_positive_eq_0.4.npz');ob=BlowupODE(D['base'],D['f'],D['g'],D['N'],D['mus']);s=ob.s;z=2

def frame(theta):
 base=np.r_[-theta,np.zeros(s+z)];basis=np.eye(1+s+z)
 b=np.array([-ob(0,base+basis[1+j],False)[0] for j in range(s)])
 j=np.argmax(abs(b));u=np.zeros(s);u[j]=1/b[j]
 K=-ob(0,np.r_[-theta,u,np.zeros(z)],False)[1:1+s]
 F=np.column_stack([ob(0,base+basis[1+s+i],False)[1:1+s] for i in range(z)])
 LL=np.column_stack([ob(0,np.r_[-theta,np.eye(s)[j],np.ones(z)],False)[1+s:] for j in range(s)])
 return b,K,F,LL[0]-LL[1]

def con(theta,r):
 b,K,FF,L=frame(theta);Fr=np.exp(r)*FF[:,0];F=Fr+FF[:,1];den=b@F
 A=np.outer(b,K)+np.outer(L,Fr)/den
 B=-np.outer(b,Fr)/den
 return A,B,F

t0=.5;r0=np.log(.00001)
rows=[]
for rout in r0+np.linspace(-1,1,5):
 solr=solve_ivp(lambda r,a:(con(t0,r)[1]@a.reshape(s,s)).ravel(),[r0,rout] if r0!=rout else [r0,rout+1e-14],np.eye(s).ravel(),rtol=1e-10,atol=1e-11)
 Tr=solr.y[:,-1].reshape(s,s)
 for tout in np.linspace(.25,.85,7):
  sol=solve_ivp(lambda t,a:(con(t,rout)[0]@a.reshape(s,s)).ravel(),[t0,tout],Tr.ravel(),rtol=1e-10,atol=1e-11)
  T=sol.y[:,-1].reshape(s,s);F=con(tout,rout)[2];row=F@T;rows.append(row/np.linalg.norm(row))
ss=np.linalg.svd(rows,compute_uv=False);print('constraint svd',ss)
