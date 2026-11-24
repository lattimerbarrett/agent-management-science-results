from pathlib import Path
exec(Path('workspace/agent4_cubic_scan.py').read_text().split('rng=np.random')[0])
import json
xsq=.8;k=1;frac=.95;sign=-1
c,b,r0,F,res0,point,x0,y0,Ex,Ey=setup(xsq);RR=Rotation.align_vectors(y0.reshape(1,3),(-x0).reshape(1,3))[0].as_matrix();zbase=y0[2]
def phi(y,inverse=False):
 if inverse:return RR.T@rot(y,np.array([0,0,1]),-k*(y[2]-zbase))
 yy=RR@y;return rot(yy,np.array([0,0,1]),k*(yy[2]-zbase))
other=np.linalg.norm(-x0+phi(-y0,True));delta=frac*other
def tau(x,y):
 yy=phi(y,True);v=x+yy;r=np.linalg.norm(v)
 if r>=delta or r<delta/4:return x,y
 t=(r-delta/4)/(3*delta/4);s=t*t*t*(10-15*t+6*t*t);angle=sign*2*np.pi*(1-s)
 return rot(x,v/r,angle),phi(rot(yy,v/r,angle))
def MAP(x,y):return tau(*F(x,y,c))
def res(q):
 xx,yy=MAP(point(q[:2],x0,Ex),point(q[2:],y0,Ey))
 return np.r_[(Ex.T@xx)/(1+xx@x0)-q[:2],(Ey.T@yy)/(1+yy@y0)-q[2:]]
rng=np.random.default_rng(147);sol=[]
for i in range(2500):
 rr=root(res,rng.normal(size=4)*rng.choice([.1,.3,1,3,10]),tol=1e-10)
 if np.linalg.norm(res(rr.x))<1e-8:
  pp=np.r_[point(rr.x[:2],x0,Ex),point(rr.x[2:],y0,Ey)]
  if all(np.linalg.norm(pp-ss)>1e-3 for ss in sol):sol.append(pp);print('root',len(sol),pp,flush=True)
sol.append(np.r_[-x0,-y0]);records=[]
for p in sol:
 x,y=p[:3],p[3:];ex=null_space(x.reshape(1,3));ey=null_space(y.reshape(1,3))
 def loc(q):
  xx=x+ex@q[:2];xx/=np.linalg.norm(xx);yy=y+ey@q[2:];yy/=np.linalg.norm(yy);fx,fy=MAP(xx,yy)
  return np.r_[ex.T@(fx-xx),ey.T@(fy-yy)]
 J=approx_derivative(loc,np.zeros(4),method='3-point',abs_step=1e-5);det=np.linalg.det(J);idx=int(np.sign(det)) if abs(det)>1e-7 else 2
 rec={'point':p.tolist(),'det':det,'index':idx,'singular_values':np.linalg.svd(J)[1].tolist()};records.append(rec);print('record',rec,flush=True)
Path('workspace/agent4_best_candidate.json').write_text(json.dumps({'xsq':xsq,'k':k,'frac':frac,'sign':sign,'other':other,'delta':delta,'C':c,'B':b,'r0':r0,'R':RR.tolist(),'records':records},indent=2))
Path('workspace/agent4_best_candidate.py').write_text(Path('scratchpad.py').read_text())