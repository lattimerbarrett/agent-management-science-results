import numpy as np,sys,itertools,time
sys.path.insert(0,'workspace');from agent2_mixed_billiards import Billiard
from agent3_delay_billiards import seed_cycle,kappa_rows
core=np.array([-3.,-2,-1,1,2,3]);start=time.time();nh=nad=0
for h in [1.,.1,3.,6.,10.,15.,17.5]:
 pol=np.poly(core);pp=pol.copy();pp[-1]+=h;roots=np.sort(np.roots(pp).real);ex=pol.copy();ex[-1]+=2*h;extrasall=np.sort(np.roots(ex).real)
 for picks in itertools.product([0,1],repeat=3):
  picks=np.array(picks);pc=np.poly(roots[2*np.arange(3)+picks]);qc=np.poly(roots[2*np.arange(3)+1-picks])
  for drop in [1,2,3,4]:
   active=np.delete(core,drop);dd=1/np.prod(np.where(np.eye(5,dtype=bool),1,active[:,None]-active[None,:]),axis=1);cc=dd*np.polyval(qc,active);left=max(active[cc<0]);right=min(active[cc>0]);eta=core[drop];extras=extrasall[extrasall>eta] if eta<left else extrasall[extrasall<eta]
   if len(extras)<3:continue
   bi=Billiard(active,extras,pc,qc,h,left,right);mm=bi.transport(tol=1e-10);U=mm['U'];Ui=np.linalg.inv(U);klkr=kappa_rows(bi);mid=(left+right)/2;Um=mm['sol'].sol(mid).reshape(3,3);Vmid=bi.mat(mid)[1]@Um
   m=len(extras);words=[list(w) for n in [1,2,3] for w in itertools.product(range(m),repeat=n) if all(w[i]!=w[i+1] for i in range(n-1))];refs=[]
   for side in ['L','R']:
    rr=[]
    for word in words:
     mat=np.eye(3)
     for j in word:mat=mm[side+'reflect'][j]@mat
     rr.append(mat)
    refs.append(rr)
   for wi,RL in enumerate(refs[0]):
    for wj,RR in enumerate(refs[1]):
     ret=RL@Ui@RR@U;vals,vec=np.linalg.eig(ret)
     for j,rho in enumerate(vals):
      if abs(rho.imag)>1e-6 or not 1e-5<rho.real<.9999:continue
      nh+=1
      for sign in [1,-1]:
       a=sign*vec[:,j].real;ar=U@a;aro=RR@ar;ali=Ui@aro
       if min(mm['Lenergy']@a,mm['Renergy']@ar,mm['Renergy']@aro,mm['Lenergy']@ali,Vmid@a,-Vmid@ali)<1e-9:continue
       good=True
       for side,ain,word in [('R',ar,words[wj]),('L',ali,words[wi])]:
        aa=ain.copy()
        for pulse in word:
         if mm[side+'growth'][pulse]@aa<=1e-8:good=False;break
         aa=mm[side+'reflect'][pulse]@aa
         if mm[side+'energy']@aa<=1e-9:good=False;break
        if not good:break
       if not good:continue
       nad+=1;ans=seed_cycle(mm,bi,a,words[wi],words[wj],klkr)
       if ans:
        print('FOUND',h,picks,drop,'extra',extras,'word',words[wi],words[wj],'rho',rho,'a',a,'seed',ans[0],flush=True);np.savez('workspace/agent3_multichannel_found.npz',core6=core,h=h,picks=picks,drop=drop,pc=pc,qc=qc,extra=extras,left=left,right=right,a=a,rho=rho,U=U,il=words[wi],ir=words[wj],S=ans[0]['S'],seed=ans[0]['z'],Lambda=ans[0]['lam']);raise SystemExit
   print('config',h,picks,drop,'elapsed',time.time()-start,'polyad',nad,flush=True)
print('none',nh,nad)
