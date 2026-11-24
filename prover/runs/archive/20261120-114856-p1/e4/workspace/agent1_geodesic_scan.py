import sys,numpy as np,json,time
sys.path.insert(0,'workspace')
from agent4_geodesic_model import GeodesicModel
from pathlib import Path
from scipy.optimize import root
rng=np.random.default_rng(771);results=[];start=time.time()
for modelidx in range(20):
 b,c=rng.uniform(.08,.62,2);d=rng.uniform(max(.7,b+.2,c+.2),.99)
 qr=np.array([-1,-b,c,d]);rr=-qr[::-1];q=np.poly(qr);r=np.poly(rr);F=np.polymul(q,r)
 cr=np.roots(np.polyder(F));cv=np.polyval(F,cr.real);H=min(cv[cv>0])*rng.uniform(.1,.8)
 try:M=GeodesicModel(q,r,H)
 except Exception:continue
 Trange=[-M.x[6]**2,-M.x[5]**2]
 rows=[]
 for tt in np.linspace(.1,.9,5):
  T=Trange[0]*(1-tt)+Trange[1]*tt
  for angle in np.linspace(-1.48,1.48,21):
   try:out=M.shoot(T,angle,tol=2e-6,maxtime=10,margin=1e-4)
   except Exception:continue
   if not out['returned'] or out['time']<1e-4:continue
   res=out['residual'];minimum=min(np.min(M.weights(tau)) for tau in out['sol'].y[:3].T)
   row=dict(T=float(T),angle=float(angle),res=res.tolist(),time=float(out['time']),minimum=float(minimum))
   rows.append(row)
 print('model',modelidx,'qroots',qr,'H',H,'returns',len(rows),'elapsed',time.time()-start,flush=True)
 if rows:
  item=dict(q=q.tolist(),r=r.tolist(),H=float(H),Trange=Trange,rows=rows);results.append(item)
  Path('workspace/agent1_geodesic_shoot_scan.json').write_text(json.dumps(results))
  for row in sorted(rows,key=lambda row:np.linalg.norm(row['res']))[:3]:
   def fun(par):
    if not Trange[0]<par[0]<Trange[1]:return np.array([10+par[0],10+par[1]])
    try:out=M.shoot(*par,tol=1e-7,maxtime=10,margin=1e-4)
    except Exception:return np.array([10,10])
    if not out['returned']:return np.array([10,10])
    return out['residual']
   rt=root(fun,[row['T'],row['angle']],tol=1e-7)
   if rt.success and np.linalg.norm(fun(rt.x))<1e-6:
    out=M.shoot(*rt.x,tol=1e-10,maxtime=20,margin=1e-6)
    minimum=min(np.min(M.weights(tau)) for tau in out['sol'].y[:3].T)
    print('CANDIDATE',rt.x,out['residual'],out['time'],minimum,flush=True)
    if out['returned'] and minimum>1e-4 and out['time']>1e-3 and np.linalg.norm(out['residual'])<1e-7:
     Path('workspace/agent1_geodesic_periodic_candidate.json').write_text(json.dumps(dict(q=q.tolist(),r=r.tolist(),H=float(H),parameters=rt.x.tolist(),res=out['residual'].tolist(),minimum=float(minimum))))
     raise SystemExit('Genuine numerical interior periodic candidate!')
