from pathlib import Path
exec(Path('workspace/agent4_cubic_scan.py').read_text().split('rng=np.random')[0])
import json
rng=np.random.default_rng(732)
for xsq in [.8,.9]:
 c,b,r0,F,res0,point,x0,y0,Ex,Ey=setup(xsq)
 RR=Rotation.align_vectors(y0.reshape(1,3),(-x0).reshape(1,3))[0].as_matrix();zbase=y0[2]
 for k in [.5,1,2,3,5]:
  def phi(y,inverse=False):
   if inverse:return RR.T@rot(y,np.array([0,0,1]),-k*(y[2]-zbase))
   yy=RR@y;return rot(yy,np.array([0,0,1]),k*(yy[2]-zbase))
  other=np.linalg.norm(-x0+phi(-y0,True))
  for frac in [.4,.7,.95]:
   delta=frac*other
   for sign in [1,-1]:
    def tau(x,y):
     yy=phi(y,True);v=x+yy;r=np.linalg.norm(v)
     if r>=delta:return x,y
     if r<delta/4:return x,y # exact 2pi rotation
     t=(r-delta/4)/(3*delta/4);s=t*t*t*(10-15*t+6*t*t);angle=sign*2*np.pi*(1-s)
     return rot(x,v/r,angle),phi(rot(yy,v/r,angle))
    def res(q):
     x=point(q[:2],x0,Ex);y=point(q[2:],y0,Ey);xx,yy=F(x,y,c);xx,yy=tau(xx,yy)
     return np.r_[(Ex.T@xx)/(1+xx@x0)-q[:2],(Ey.T@yy)/(1+yy@y0)-q[2:]]
    sol=[]
    for i in range(100):
     rr=root(res,rng.normal(size=4)*rng.choice([.3,1,3]),tol=1e-9)
     if np.linalg.norm(res(rr.x))<1e-7:
      pp=np.r_[point(rr.x[:2],x0,Ex),point(rr.x[2:],y0,Ey)]
      if all(np.linalg.norm(pp-ss)>1e-3 for ss in sol):sol.append(pp)
     if len(sol)>=10:break
    print('x,k,frac,sign,other,roots',xsq,k,frac,sign,other,len(sol)+1,flush=True)
    if len(sol)<=3:Path(f'workspace/agent4_tau_candidate_{xsq}_{k}_{frac}_{sign}.json').write_text(json.dumps({'x':xsq,'k':k,'frac':frac,'sign':sign,'roots':[pp.tolist() for pp in sol]}))
Path('workspace/agent4_tau_search.py').write_text(Path('scratchpad.py').read_text())