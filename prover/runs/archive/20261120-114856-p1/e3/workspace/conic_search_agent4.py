from pathlib import Path
src=Path('workspace/word_search_agent4.py').read_text();exec(src[:src.index('rng=')])
def QGs(a,L,H,co):
 v=a+L;d=a*L;out=[]
 for mm,lam0 in [(1-co[2],co[2]),(1-co[1],co[1])]:
  mp=mm+v-1;V=mm-mm*mm;Vp=v*mp-d-mp*mp;th=-mm/V+mp/Vp;tz=1/V-1/Vp;E=np.array([-d,v-1]);ta=np.array([th,tz]);G=np.column_stack([ta-lam0*E/H,E/H]);G=(G+G.T)/2
  BC=d+(v-1)*(mm-1);TT=np.array([[-d,v-1],[-d*mm/np.sqrt(H),BC/np.sqrt(H)]]);Ti=np.linalg.inv(TT);out.append(Ti.T@G@Ti)
 return out
rng=np.random.default_rng(729);found=[];t=time.time()
for case in range(2000):
 if case%2:a=rng.uniform(.02,.98);L=1+10**rng.uniform(-.7,1.7)
 else:a,L=np.sort(rng.uniform(.001,.999,2))
 v=a+L;d=a*L;Q=np.poly([0,a,1,L]);crit=np.sort(np.roots(np.polyder(Q)));lev=np.polyval(Q,crit);H=10**rng.uniform(-5,-.01)*min(-lev[0],lev[1],-lev[2]);co,ex,ml,mr,F,refs=data(a,L,H);GL,GR=QGs(a,L,H,co)
 sigma=10**rng.uniform(-5,5,3000);tt=10**rng.uniform(-5,5,3000);X=np.array([-np.ones(len(sigma)),sigma]).T;Ydir=np.array([-np.ones(len(tt)),-tt]).T
 qx=np.einsum('bi,ij,bj->b',X,GL,X);qy=np.einsum('bi,ij,bj->b',Ydir,GL,Ydir);al=np.sqrt(np.maximum(qx/qy,0));Y=Ydir*al[:,None];FX=X@F.T;FY=Y@F.T;qr=np.einsum('bi,ij,bj->b',FY,GR,FY);den=np.einsum('bi,ij,bj->b',FX,GR,FX);rho=np.sqrt(np.maximum(qr/den,0));W=FX*rho[:,None]
 sl=(Y[:,1]-X[:,1])/(Y[:,0]-X[:,0]);sr=(W[:,1]-FY[:,1])/(W[:,0]-FY[:,0]);leftslopes=np.array([b[1]/b[0]for R,b,ell in refs[0]]);rightslopes=np.array([b[1]/b[0]for R,b,ell in refs[1]])
 good=(qx/qy>0)&(qr/den>0)&(al>0)&(al<1)&(FY[:,0]<0)&(FX[:,0]<0)&(rho>0)&(rho<1)&(W[:,0]>FY[:,0])&(sl>leftslopes.min())&(sl<leftslopes.max())&(sr>rightslopes.min())&(sr<rightslopes.max())
 if good.any():
  ii=np.where(good)[0][0];print('FOUND',case,a,L,H,'rho',rho[ii],'X,Y',X[ii],Y[ii],flush=True);found.append((a,L,H,X[ii],Y[ii],rho[ii],co,ex,F,refs,GL,GR));pickle.dump(found,open('workspace/conic_found_agent4.pkl','wb'))
print('DONE',len(found),time.time()-t)
Path('workspace/conic_search_agent4.py').write_text(Path('scratchpad.py').read_text())
