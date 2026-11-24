import numpy as np
from itertools import product,permutations
from numpy.polynomial.legendre import leggauss
rng=np.random.default_rng(118)
S=4;HVAL=.1
GQ,GW=leggauss(20)

def setup(pc,qc):
    prod=np.polymul(pc,qc);plus=prod.copy();minus=prod.copy();plus[-1]-=HVAL;minus[-1]+=HVAL
    co=np.roots(plus);ex=np.roots(minus)
    if max(abs(co.imag))>1e-7 or max(abs(ex.imag))>1e-7:return
    co=np.sort(co.real);ex=np.sort(ex.real);pv=np.polyval(pc,co);qv=np.polyval(qc,co)
    pd=np.prod(np.where(np.eye(8,dtype=bool),1,co[:,None]-co[None,:]),axis=1)
    signs=np.sign(qv/pd);gaps=np.where(signs[1:]!=signs[:-1])[0]
    if len(gaps)!=3 or signs[0]>0:return
    V={};E={}
    for bits in product(range(2),repeat=3):
        mis=tuple(gaps+np.array(bits));hf=np.prod(co[:,None]-co[list(mis)],axis=1);w=qv*hf/pd
        if min(w)<-1e-8:return
        X=np.vander(co,4,increasing=True);A=(X.T*w)@X;Ap=(X.T*(w*pv*pv/HVAL))@X
        M=np.linalg.solve(Ap,A);L=(w*(pv-qv))@X
        R=qv[:,None]*X-(pv[:,None]*X)@M+L
        Xe=np.vander(ex,4,increasing=True);pe=np.polyval(pc,ex);qe=np.polyval(qc,ex)
        Re=qe[:,None]*Xe-(pe[:,None]*Xe)@M+L;D=(4*L-2*Re)/HVAL
        F=4*np.linalg.solve(A,Xe.T*pe)
        refl=[]
        for j in range(8):
            den=D[j]@F[:,j]
            refl.append(np.eye(4)-2*np.outer(F[:,j],D[j])/den)
        V[bits]=dict(mis=mis,g=np.vstack((2*R/HVAL,D)),L=L,refl=refl)
    for bits in product(range(2),repeat=3):
      for dim in range(3):
        if bits[dim]:continue
        fixed=[gaps[j]+bits[j] for j in range(3) if j!=dim]
        inds=np.array([i for i in range(8) if i not in fixed]);t=co[inds];X=np.vander(t,4,increasing=True)
        p=np.polyval(pc,t);q=np.polyval(qc,t);der=np.prod(np.where(np.eye(6,dtype=bool),1,t[:,None]-t[None,:]),axis=1)
        left,right=co[gaps[dim]],co[gaps[dim]+1]
        mid=(left+right)/2;w=q*(t-mid)/der;wt=-q/der
        A=(X.T*w)@X;Ap=(X.T*(w*p*p/HVAL))@X;M=np.linalg.solve(Ap,A);L=(w*(p-q))@X
        R=q[:,None]*X-(p[:,None]*X)@M+L
        vel=wt@(2*w[:,None]*R/HVAL)/(wt@wt)
        cov=vel*np.polyval(qc,mid)/np.prod(mid-t)
        u=np.zeros(4)
        for xx,ww in zip(GQ,GW):
            th=mid+(right-left)*xx/2;w=q*(t-th)/der;A=(X.T*w)@X
            fac=np.sqrt(np.polyval(qc,th)*np.polyval(pc,left)/(np.polyval(pc,th)*np.polyval(qc,left)))
            u+=ww*(right-left)/2*HVAL/(4*np.polyval(qc,th))*np.linalg.solve(A,np.array([1,th,th*th,th**3]))*fac
        U=np.eye(4)+np.outer(u,cov)
        E[(bits,dim)]=(U,vel)
    return co,ex,V,E

def search(pc,qc):
 out=setup(pc,qc)
 if out is None:return None
 co,ex,V,E=out;best=None;nrays=0
 for start in product(range(2),repeat=3):
  for perm in permutations(range(3)):
   path=[start];Us=[];vels=[]
   for dim in perm:
    b=path[-1];base=list(b);base[dim]=0;base=tuple(base);U,v=E[(base,dim)]
    Us.append(U if b[dim]==0 else np.linalg.inv(U));vels.append(v*(1 if b[dim]==0 else -1))
    bb=list(b);bb[dim]=1-bb[dim];path.append(tuple(bb))
   U=Us[2]@Us[1]@Us[0];Ui=np.linalg.inv(U);A=V[start];D=V[path[-1]]
   for j,xi in enumerate(ex):
    SA=A['refl'][j];SD=D['refl'][j];M=Ui@SD@U@SA
    vals,vecs=np.linalg.eig(M)
    for ii,rho in enumerate(vals):
     if abs(rho.imag)>1e-7 or not(1e-6<rho.real<.999999):continue
     a=vecs[:,ii].real;a*=np.sign(A['L']@a)
     if A['L']@a<1e-10:continue
     a/=A['L']@a
     # Three independent incoming logarithmic seeds: two dormant core modes and one outside.
     ent=A['mis'][perm[0]];seedrows=[i for i in A['mis'] if i!=ent]+[8+j]
     K=np.zeros((16,3));K[seedrows]=np.eye(3);ineq=[];ok=True
     def phase(b,a,kind,ent,ext=None):
      nonlocal K,ok
      vv=V[b];inds=list(vv['mis'])+[8+j];rates=vv['g']@a
      if vv['L']@a<=1e-8:ok=False;return a
      if kind=='switch':
       if rates[ent]>=-1e-8 or rates[ext]<=1e-8:ok=False;return a
       waits=[(ext,rates[ext])]
      else:
       if rates[ent]>=-1e-8 or rates[8+j]<=1e-8:ok=False;return a
       waits=[(8+j,rates[8+j])]
      for row,rate in waits:
       dt=K[row]/rate;ineq.append(dt.copy());K[inds]-=np.outer(rates[inds],dt)
       ineq.extend(K[i].copy() for i in inds if i!=row)
      if kind=='pulse':
       a=vv['refl'][j]@a;rates=vv['g']@a
       if rates[ent]<=1e-8 or rates[8+j]>=-1e-8 or vv['L']@a<=1e-8:ok=False;return a
       dt=K[ent]/rates[ent];ineq.append(dt.copy());K[inds]-=np.outer(rates[inds],dt)
       ineq.extend(K[i].copy() for i in inds if i!=ent)
      return a
     a=phase(start,a,'pulse',ent)
     for k in range(3):
      if not ok:break
      if vels[k]@a<=1e-8:ok=False;break
      a=Us[k]@a;b=path[k+1];ent=V[b]['mis'][perm[k]];K[ent]=0
      if k<2:a=phase(b,a,'switch',ent,V[b]['mis'][perm[k+1]])
     if not ok:continue
     a=phase(path[-1],a,'pulse',ent)
     for k in range(2,-1,-1):
      if not ok:break
      if vels[k]@np.linalg.solve(Us[k],a)>=-1e-8:ok=False;break
      a=np.linalg.solve(Us[k],a);b=path[k];ent=V[b]['mis'][perm[k]];K[ent]=0
      if k>0:a=phase(b,a,'switch',ent,V[b]['mis'][perm[k-1]])
     if not ok:continue
     nrays+=1;Seed=K[seedrows];ee,zz=np.linalg.eig(Seed)
     for kk,lam in enumerate(ee):
      if abs(lam.imag)>1e-7 or lam.real<=1.00001:continue
      z=zz[:,kk].real;z*=np.sign(z.sum());z/=z.sum()
      if min(z)<=0:continue
      margin=min(np.array(ineq)@z)
      if best is None or margin>best['margin']:best=dict(margin=margin,rho=rho.real,Lambda=lam.real,seed=z,xi=xi,pc=pc,qc=qc,start=start,perm=perm,Seed=Seed)
      if margin>1e-8:return best,nrays
 return best,nrays

basep=np.array([1.,0.,-5.,0.,3.]);baseq=np.array([1.,0.,-5.,0.,4.])
for k in range(18):
 pc=basep.copy();qc=baseq.copy()
 if k:
  pc[1:]+=rng.normal(size=4)*np.array([.09,.06,.12,.025]);qc[1:]+=rng.normal(size=4)*np.array([.09,.06,.12,.025])
 result=search(pc,qc)
 print('trial',k,'symmetric' if k==0 else 'asymmetric','result',result,flush=True)
 if result and result[0] is not None:
  np.save('s4_asymmetric_transition_candidate.npy',result,allow_pickle=True)
  if result[0]['margin']>1e-8:break
