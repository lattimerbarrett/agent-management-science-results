import numpy as np,itertools,sys,time,warnings
sys.path.insert(0,'workspace');from agent4_lshape import check
rng=np.random.default_rng(35);start=time.time();count=0
for it in range(500):
 core=np.r_[-1.,np.sort(rng.uniform(-.9,.9,4)),1.]
 if min(np.diff(core))<.055:continue
 ch=np.poly(core);cr=np.sort(np.roots(np.polyder(ch)).real);mn=min(-np.polyval(ch,cr[[0,2,4]]));h=mn*10**rng.uniform(-3,-.001);pol=ch.copy();pol[-1]+=h;r=np.sort(np.roots(pol).real);pol[-1]+=h;ex=np.roots(pol);ex=ex.real[abs(ex.imag)<1e-8]
 for picks in itertools.product([0,1],repeat=3):
  pc=np.poly(r[[2*j+picks[j]for j in range(3)]]);qc=np.poly(r[[2*j+1-picks[j]for j in range(3)]])
  for xi in ex:
   try:res=check(core,pc,qc,h,xi)
   except (ValueError,np.linalg.LinAlgError,ZeroDivisionError):continue
   count+=1
   if res:
    print('HIT',it,h,picks,xi,'core',core,res,flush=True);np.savez('workspace/agent4_lshape_found.npz',core=core,pc=pc,qc=qc,h=h,xi=xi,picks=picks,**res);raise SystemExit
 if it%25==0:print(it,count,time.time()-start,flush=True)
print('NOHIT',count,time.time()-start)
