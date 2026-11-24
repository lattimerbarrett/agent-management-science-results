from pathlib import Path
src=Path('workspace/conic_search_agent4.py').read_text();exec(src[:src.index('rng=np.random')]);rng=np.random.default_rng(346);found=[];tt=time.time()
for case in range(20000):
 if case%2:a=rng.uniform(.0001,.9999);L=1+10**rng.uniform(-4,2)
 else:a,L=np.sort(rng.uniform(.0001,.9999,2))
 Q=np.poly([0,a,1,L]);crit=np.sort(np.roots(np.polyder(Q)));lev=np.polyval(Q,crit);H=10**rng.uniform(-8,-.0001)*min(-lev[0],lev[1],-lev[2])
 try:co,ex,ml,mr,F,refs=data(a,L,H);GL,GR=QGs(a,L,H,co)
 except (ValueError,np.linalg.LinAlgError):continue
 for side in range(2):
  # side0 continuous left+single right, side1 continuous right+single left
  C=np.diag([1,(-1)**side]);GG=C@(GL if side==0 else GR)@C;FF=C@(F if side==0 else np.linalg.inv(F))@C;multi=[(C@R@C,C@b,ell@C) for R,b,ell in refs[side]];single=[(C@R@C,C@b,ell@C)for R,b,ell in refs[1-side]]
  sg=10**rng.uniform(-7,7,1000);X=np.c_[-np.ones(len(sg)),sg];qx=np.einsum('bi,ij,bj->b',X,GG,X);FX=X@FF.T
  for jj,(RR,bb,el)in enumerate(single):
   NN=np.linalg.solve(FF,RR@FF);YD=X@NN.T;qyd=np.einsum('bi,ij,bj->b',YD,GG,YD);rho=np.sqrt(np.maximum(qx/qyd,0));Y=rho[:,None]*YD;FY=Y@FF.T;W=rho[:,None]*FX
   active=np.array([(X@ell>1e-8)&(Y@ell< -1e-8)for R,b,ell in multi]).T;slopes=np.array([b[1]/b[0]for R,b,ell in multi]);lo=np.min(np.where(active,slopes[None,:],np.inf),axis=1);hi=np.max(np.where(active,slopes[None,:],-np.inf),axis=1);ds=(Y[:,1]-X[:,1])/(Y[:,0]-X[:,0]);good=(qx/qyd>0)&(rho>1e-5)&(rho<.99999)&(Y[:,0]<0)&(Y[:,0]>-1)&(Y[:,1]<0)&(FY[:,0]<0)&(W[:,0]>FY[:,0])&(FY@el>1e-8)&(active.sum(1)>=2)&(ds>lo+1e-8)&(ds<hi-1e-8)
   if good.any():
    ii=np.where(good)[0][0];item=(a,L,H,side,jj,X[ii],Y[ii],rho[ii],co,ex,F,refs,GL,GR,active[ii]);found.append(item);print('FOUND',case,'aLH',a,L,H,'sidej',side,jj,'XYrho',X[ii],Y[ii],rho[ii],'active',active[ii],flush=True);pickle.dump(found,open('workspace/mixed_conic_found_agent4.pkl','wb'));break
 if case%1000==0:print('progress',case,'found',len(found),'time',time.time()-tt,flush=True)
print('DONE',len(found),time.time()-tt)
Path('workspace/mixed_conic_search_agent4.py').write_text(Path('scratchpad.py').read_text())
