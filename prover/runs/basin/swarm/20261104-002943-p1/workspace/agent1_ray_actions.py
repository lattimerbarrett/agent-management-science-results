import numpy as np,pickle
rays=pickle.load(open('workspace/agent4_broad_positive_rays.pkl','rb'))

def factory(d):
 x=np.r_[d['act'],d['mus']];p=np.r_[d['p'],d['pm']];q=np.r_[d['q'],d['qm']];C=float(d['C']);w0=np.r_[d['w'],[0,0]];V=x[:,None]**np.arange(4);T=np.r_[-w0[:6]/x[:6],[0,0]];Vm=V[6:];pm=p[6:];qm=q[6:]
 def field(z):
  pos=z[0];hf=z[1:4];A=z[4:];w=w0+pos*T;erow=-(w*p**3)@V/C;hc=np.r_[(1-erow[1:]@hf)/erow[0],hf];h=V@hc;u=w*p*h;M=V.T@(w[:,None]*V);N=V.T@((w*p*p/C)[:,None]*V);ac=-C*np.linalg.solve(M,N@hc);aa=V@ac;F=np.dot(u,p*p);rat=2*(aa/p+C*h/q-F/C);b=w*rat;vel=T@b/(T@T)
  bb=-V@np.linalg.solve(M,V.T@(u*aa));e=u@(p*aa);zz=w*p*p/C;z1=(u*p*p+2*w*p*aa-zz*F)/C;z2=(w*(aa*aa+2*p*bb)+2*u*p*aa-z1*F-zz*e)/C
  aaa=C*h;bbb=-V@np.linalg.solve(N,V.T@(z2*q+z1*aaa));eee=z2@(q*q)+z1@(q*aaa);f2=(z2*q*q+2*z1*q*aaa+zz*(aaa*aaa+2*q*bbb)-(u+b)*F-w*eee)/C
  hd=np.linalg.solve(C*N,V.T@(p*(f2-b*p*h)));hd+=np.linalg.solve(N,Vm.T@(4*pm/C*A*A));ad=A*(-(pm*(C*(Vm@hc))+qm*(Vm@ac)+F)/C)
  c=(np.sum((C+p[:6]**2)*b[:6]**2/w[:6])/4+4*np.sum((C+pm**2)*A*A))/C
  return np.r_[vel,(hd+c*hc)[1:],ad+c*A]
 E=d['E'];eq=np.r_[0,d['h'][1:]/E,d['A']/E]
 return field,eq

def jac(field,z):return np.column_stack([field(z+1e-20j*np.eye(6)[j]).imag/1e-20 for j in range(6)])

def actions(d):
 field,eq=factory(d);J=jac(field,eq);vals,R=np.linalg.eig(J);vl,L=np.linalg.eig(J.T);c=d['c'];ir=np.argmin(abs(vals-c));il=np.argmin(abs(vl-c));ell=L[:,il].real;ell/=np.dot(ell,R[:,ir].real)
 inds=[j for j in range(6) if vals[j].imag>1e-5];out=[]
 for j in inds:
  v=R[:,j];v/=np.linalg.norm(v);a=v.real;b=v.imag;cs=[]
  for step in [1e-3,1e-4,1e-5]:
   H=((jac(field,eq+step*a)-jac(field,eq-step*a))@a+(jac(field,eq+step*b)-jac(field,eq-step*b))@b)/(2*step);cs.append(float(ell@H))
  out.append((vals[j],cs))
 return np.linalg.norm(field(eq)),out

if __name__=='__main__':
 results=[]
 for j,d in enumerate(rays):
  err,out=actions(d);print(j,'Lr',d['L'],d['ratio'],d['bits'],'err',err,'actions',out,flush=True);results.append((j,err,out))
 pickle.dump(results,open('workspace/agent1_ray_actions_results.pkl','wb'))