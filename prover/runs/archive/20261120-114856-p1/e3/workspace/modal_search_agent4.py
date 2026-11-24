from pathlib import Path
src=Path('workspace/word_search_agent4.py').read_text();exec(src[:src.index('rng=')].replace('depth=4','depth=3').replace('ivcont=constrain(ivn,side*MM[1])','ivcont=ivn'))
rng=np.random.default_rng(972);found=[];t=time.time();maxstates=0
for case in range(5000):
 if case%2:a=rng.uniform(.02,.98);L=1+10**rng.uniform(-1.5,1.5)
 else:a,L=np.sort(rng.uniform(.001,.999,2))
 v=a+L;d=a*L;Q=np.poly([0,a,1,L]);crit=np.sort(np.roots(np.polyder(Q)));lev=np.polyval(Q,crit);H=10**rng.uniform(-5,-.001)*min(-lev[0],lev[1],-lev[2]);co,ex,ml,mr,F,refs=data(a,L,H);Fback=np.linalg.inv(F);ws=[words(refs[0],1),words(refs[1],-1)]
 states=[(np.eye(2),(0,np.inf),())]
 for depth in range(20):
  side=depth%2;fl=F if side==0 else Fback;nxt=[]
  for M,iv,history in states:
   for word,W,ivlocal in ws[side]:
    ivn=constrain(iv,-M[0])
    if ivn is None:continue
    if np.isfinite(ivlocal[0]):ivn=constrain(ivn,M[1]+ivlocal[0]*M[0])
    if ivn is None:continue
    if np.isfinite(ivlocal[1]):ivn=constrain(ivn,-M[1]-ivlocal[1]*M[0])
    if ivn is None:continue
    Mn=fl@W@M;ivn=constrain(ivn,-Mn[0])
    if ivn is None:continue
    hist=history+(word,);nxt.append((Mn,ivn,hist))
    if side==1:
     vals,vecs=np.linalg.eig(Mn)
     for ei in range(2):
      val=vals[ei]
      if abs(val.imag)>1e-7 or not 1e-5<val.real<1-1e-5:continue
      x=vecs[:,ei].real;x*=-np.sign(x[0]);sigma=x[1]/(-x[0])
      if ivn[0]<sigma<ivn[1]:
       print('FOUND',case,'a,L,H',a,L,H,'depth',depth+1,'history',hist,'rho',val,'x',x,'iv',ivn,flush=True);found.append((a,L,H,hist,val,x,co,ex,F,refs));pickle.dump(found,open('workspace/modal_found_agent4.pkl','wb'))
  states=nxt;maxstates=max(maxstates,len(states))
  if not states:break
  if len(states)>10000:break
 if case%500==0:print('progress',case,'time',time.time()-t,'maxstates',maxstates,flush=True)
print('DONE',len(found),time.time()-t)
Path('workspace/modal_search_agent4.py').write_text(Path('scratchpad.py').read_text())
