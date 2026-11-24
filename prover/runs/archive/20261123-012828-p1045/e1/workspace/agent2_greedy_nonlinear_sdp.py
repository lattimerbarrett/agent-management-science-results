import numpy as np
from scipy.optimize import linprog,minimize
from itertools import combinations_with_replacement
pairs=list(combinations_with_replacement(range(3),2));idx={p:i for i,p in enumerate(pairs)}
def optimize(A,r):
 s=1-r;n=19;cstar=max(.5,4*np.sqrt(A/3)-2*A,2*np.sqrt(A)-A)
 Q=r*(A-r);h0=Q/s;H0=cstar-2*np.sqrt(r*h0)+h0;h1=Q/H0;H1=cstar-2*np.sqrt(r*h1)+h1
 Mb=np.zeros((4,4,n));Mr=np.zeros_like(Mb);Hb=np.zeros((3,3,n));K_b=np.zeros((4,4));K_r=K_b.copy();K_b[0,0]=s;K_r[0,0]=r
 for i in range(3):
  Mb[0,i+1,1+i]=Mb[i+1,0,1+i]=1
  Mr[0,i+1,4+i]=Mr[i+1,0,4+i]=1
 for (i,j),q in idx.items():
  Mb[i+1,j+1,7+q]=Mb[j+1,i+1,7+q]=1
  Mr[i+1,j+1,13+q]=Mr[j+1,i+1,13+q]=1
  Hb[i,j,7+q]=Hb[j,i,7+q]=1 if i==j else -1
 rows=[];bs=[]
 def add(row,b):rows.append(row);bs.append(b)
 for i in range(3):
  row=np.zeros(n);row[0]=1;row[1+i]=-2;row[4+i]=-2;row[7+idx[i,i]]=1;row[13+idx[i,i]]=1;add(row,0)
 for (i,j),q in idx.items():
  if i!=j:
   row=np.zeros(n);row[7+q]=row[13+q]=1;add(row,A)
  for t in [i,j]:
   row=np.zeros(n);row[7+q]=1;row[1+t]=-1;add(row,0)
   row=np.zeros(n);row[13+q]=1;row[4+t]=-1;add(row,0)
 for i,h in [(0,h0),(1,h1)]:
  row=np.zeros(n);row[13+idx[i,i]]=1;add(row,h)
 fun=np.zeros(n);fun[0]=-1
 for it in range(1000):
  sol=linprog(fun,A_ub=rows,b_ub=bs,bounds=[(.5,1)]+[(0,s)]*3+[(0,r)]*3+[(0,s)]*6+[(0,r)]*6,method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
  if not sol.success:return None,H0+H1-s
  worst=0
  for M,K in [(Mb,K_b),(Mr,K_r),(Hb,np.zeros((3,3)))]:
   H=np.einsum('ijk,k->ij',M,sol.x)+K;ev,V=np.linalg.eigh(H);worst=min(worst,ev[0])
   if ev[0]<-1e-9:
    v=V[:,0];add(-np.einsum('i,j,ijk->k',v,v,M),v@K@v)
  if worst>=-1e-8:
   break
 def nonlinear(z):
  q0=z[13+idx[0,0]];q1=z[13+idx[1,1]];q2=z[13+idx[2,2]]
  hh0=cstar-2*np.sqrt(max(0,r*q0))+q0
  hh1=cstar-2*np.sqrt(max(0,r*q1))+q1
  mm=max(0,hh0+hh1-s)
  cs=[Q-hh0*q1-(s-hh0)*q0,Q-mm*q2-(s-mm)*q0,q1-q0,q2-q1]
  for M,K in [(Mb,K_b),(Mr,K_r),(Hb,np.zeros((3,3)))]:
   H=np.einsum('ijk,k->ij',M,z)+K;cs.extend(np.linalg.eigvalsh(H))
  return np.r_[np.array(bs)-np.array(rows)@z,cs]
 opt=minimize(lambda z:-z[0],sol.x,bounds=[(.5,1)]+[(0,s)]*3+[(0,r)]*3+[(0,s)]*6+[(0,r)]*6,constraints=[{'type':'ineq','fun':nonlinear}],method='SLSQP',options={'ftol':1e-12,'maxiter':1000})
 if np.min(nonlinear(opt.x))<-1e-6:print('SLSQP error',opt.message,np.min(nonlinear(opt.x)))
 return opt.x[0],H0+H1-s
 return sol.x[0],H0+H1-s
if __name__=='__main__':
 for A in [1/12,.085,.09,.095729]:
  for r in [A*.01,A*.1,A*.5,A*.75,A*.99]:
   c,inter=optimize(A,r)
   print(A,r,'c',c,'goal',max(.5,4*np.sqrt(A/3)-2*A,2*np.sqrt(A)-A),'inter',inter,flush=True)
