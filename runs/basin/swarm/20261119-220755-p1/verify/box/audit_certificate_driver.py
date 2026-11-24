"""Rigorous adaptive pointwise certificate for the s4 periodic orbit.
This is a long run (~20-40min on two workers). All inputs float Hermite data
are interpreted as exact dyadic rationals; all bounds are directed intervals.
"""
import sys,os,json,time,hashlib,multiprocessing as mproc
from pathlib import Path
import numpy as np
sys.path.insert(0,'workspace')
from sage.all import RealIntervalField
from agent4_interval_blowup import IntervalBlowup
from agent4_floquet_pointwise import FloquetPointwiseBounds
SOURCE='workspace/agent2_floquetframe_m072.npz'
OUT=Path('recomputed_certificate');OUT.mkdir(exist_ok=True)
RHO=6e-5
TARGET={'delta':3.7e-6,'E':.001,'H':1500.,'b':500.,'a_normal':.0001}

def initialize():
 global ENGINE,DATA
 DATA=np.load(SOURCE);ob=IntervalBlowup(q1='-18/25',kind='interval',bits=300)
 ENGINE=FloquetPointwiseBounds(ob,DATA['x'],DATA['gamma_values'],DATA['gamma_derivs'],DATA['frame_values'],DATA['frame_derivs'],float(DATA['T']),DATA['D'])

def up(x):return float(np.nextafter(float(x),np.inf))
def down(x):return float(np.nextafter(float(x),-np.inf))
def work(job):
 lo,hi=job;recs=[];evaluations=0;largest_depth=0
 for i in range(lo,hi):
  stack=[(float(DATA['x'][i]),float(DATA['x'][i+1]),0)]
  while stack:
   a,b,depth=stack.pop();rr=ENGINE.bound(a,b,rho=RHO);evaluations+=1;largest_depth=max(largest_depth,depth)
   good=all(rr[k]<=v for k,v in TARGET.items()) and rr['a0_lower']>=.9999
   good=good and rr['physical_tube'][0].lower()>0 and rr['physical_tube'][0].upper()<1 and all(z.lower()>0 for z in rr['physical_tube'][5:])
   if good:
    rec={'index':i,'left':a,'right':b,'depth':depth}
    for k in TARGET:rec[k]=up(rr[k])
    rec['a0_lower']=down(rr['a0_lower']);rec['theta_lower']=down(rr['physical_tube'][0].lower());rec['theta_upper']=up(rr['physical_tube'][0].upper())
    rec['Z0_lower']=down(rr['physical_tube'][5].lower());rec['Z1_lower']=down(rr['physical_tube'][6].lower())
    recs.append(rec)
   elif depth<10:
    mid=(a+b)/2;stack.extend([(mid,b,depth+1),(a,mid,depth+1)])
   else:
    fail={'job':job,'i':i,'left':a,'right':b,'depth':depth,'bounds':{k:up(rr[k]) for k in TARGET},'a0':down(rr['a0_lower'])}
    (OUT/f'FAIL_{i}.json').write_text(json.dumps(fail,indent=2));raise RuntimeError(str(fail))
 result={'lo':lo,'hi':hi,'evaluations':evaluations,'maxdepth':largest_depth,'records':recs,'source_sha256':hashlib.sha256(Path(SOURCE).read_bytes()).hexdigest()}
 (OUT/f'chunk_{lo:04d}_{hi:04d}.json').write_text(json.dumps(result))
 return len(recs),evaluations,largest_depth

def main():
 data=np.load(SOURCE);n=len(data['x'])-1;started=time.time()
 jobs=[(lo,min(lo+10,n)) for lo in range(0,n,10)]
 # Existing chunks are reusable only if they have exactly the same source hash.
 sha=hashlib.sha256(Path(SOURCE).read_bytes()).hexdigest();pending=[]
 for lo,hi in jobs:
  file=OUT/f'chunk_{lo:04d}_{hi:04d}.json'
  if file.exists() and json.loads(file.read_text()).get('source_sha256')==sha:continue
  pending.append((lo,hi))
 if pending:
  with mproc.get_context('fork').Pool(2,initializer=initialize) as pool:
   for j,res in enumerate(pool.imap_unordered(work,pending),1):
    if j%10==0:print('chunks',j,'/',len(pending),'last',res,'seconds',time.time()-started,flush=True)
 records=[];evaluations=0
 for lo,hi in jobs:
  x=json.loads((OUT/f'chunk_{lo:04d}_{hi:04d}.json').read_text());assert x['source_sha256']==sha
  records+=x['records'];evaluations+=x['evaluations']
 # Ensure the accepted intervals exactly tile each original Hermite piece.
 for i in range(n):
  rows=sorted((r for r in records if r['index']==i),key=lambda r:r['left'])
  assert rows[0]['left']==float(data['x'][i]) and rows[-1]['right']==float(data['x'][i+1])
  assert all(a['right']==b['left'] for a,b in zip(rows[:-1],rows[1:]))
 maxima={k:max(r[k] for r in records) for k in TARGET};a0=min(r['a0_lower'] for r in records)
 summary=dict(maxima=maxima,a0_lower=a0,records=len(records),evaluations=evaluations,source_sha256=sha,
  theta_lower=min(r['theta_lower'] for r in records),theta_upper=max(r['theta_upper'] for r in records),
  Z0_lower=min(r['Z0_lower'] for r in records),Z1_lower=min(r['Z1_lower'] for r in records),rho=RHO)
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2))
 # Audited tube-theorem inequalities, using conservative exact alpha=1/6.
 I=RealIntervalField(300);sf=I(2).sqrt();delta=sf*I(maxima['delta']);e=sf*I(maxima['E']);H=sf*I(maxima['H']);b=sf*I(maxima['b']);a=sf*I(maxima['a_normal']);astar=I(a0);rho=I(RHO);alpha=I(1)/6;d0=I(20)
 DD=data['D'];assert min(abs(float(DD[i,i])) for i in range(1,7))>1/6
 assert DD[5,5]==DD[6,6] and DD[5,6]==-DD[6,5]
 assert np.count_nonzero(DD-np.diag(np.diag(DD)))-2==0
 assert DD[0,0]==0 and all(I(abs(float(DD[i,i]))).lower()>alpha.upper() for i in range(1,7))
 assert sf.upper()*max(sum(abs(I(float(DD[i,j]))).upper() for j in range(1,7)) for i in range(1,7))<d0.lower()
 assert I(float(data['T'])).lower()>0
 rr=delta+e*rho+H*rho**2/2;den=astar-b*rho;qbar=rr/den;qlip=(e+H*rho+b*qbar)/den
 Nbar=rr+(a+(b+d0)*rho)*qbar;fbar=Nbar/(1-qbar)
 LipN=e+H*rho+(b+d0)*qbar+(a+(b+d0)*rho)*qlip
 Lipf=LipN/(1-qbar)+Nbar*qlip/(1-qbar)**2
 assert den.lower()>0 and qbar.upper()<1 and fbar.upper()<(alpha*rho).lower() and Lipf.upper()<alpha.lower()
 # Explicit nonconstancy and positive base-weights checks on the certified tube.
 initialize()
 imin=int(np.argmin(data['gamma_values'][:,0]));imax=int(np.argmax(data['gamma_values'][:,0]))
 lowpoint=ENGINE.bound(float(data['x'][imin]),float(data['x'][imin]),hessian=False,rho=RHO)['physical_tube'][0]
 highpoint=ENGINE.bound(float(data['x'][imax]),float(data['x'][imax]),hessian=False,rho=RHO)['physical_tube'][0]
 assert lowpoint.upper()<highpoint.lower()
 th=I(summary['theta_lower'],summary['theta_upper']);oo=ENGINE.ob
 pbase=[oo.N*(oo.nodes[j]-th)/(oo.d[j]*oo.fv[j]) for j in range(6)]
 assert all(p.lower()>0 for p in pbase)
 assert all((oo.mus[j]+4).lower()>0 for j in range(2))
 print('NONCONSTANCY point intervals',lowpoint,highpoint,'min baseweight',min(p.lower() for p in pbase))
 print('CERTIFIED SUMMARY',summary)
 print('TUBE INEQUALITIES: fbar',fbar,'alpha*rho',alpha*rho,'Lipf',Lipf,'alpha',alpha)
 print('RIGOROUS POSITIVE HYPERBOLIC NONCONSTANT PERIODIC ORBIT CERTIFIED')

if __name__=='__main__':main()
