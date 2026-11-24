import numpy as np,itertools,json
# Generic reflection/edge necessary-cycle search; not a rigorous orbit realization.
from scipy.integrate import solve_ivp
x8=np.array([-8,-7,-4,-1,1,4,7,8])/8;p=np.array([1.,0,-65/64,0,424/4096]);L=360/4096;inds=np.array([0,1,4,5,6,7]);x=x8[inds];P=np.poly(x);den=np.polyval(np.polyder(P),x);f=np.vander(x,4,increasing=True);a=x8[5];b=x8[6];records=[];tested=0
rng=np.random.default_rng(448)
for gi in range(100):
 gaps=np.exp(rng.uniform(-1,1,3));centers=np.r_[0,np.cumsum(gaps)];centers-=np.mean(centers);centers/=max(abs(centers));local=np.r_[gaps[0],np.minimum(gaps[:-1],gaps[1:]),gaps[-1]]/max(abs(np.r_[0,np.cumsum(gaps)]-np.mean(np.r_[0,np.cumsum(gaps)])));widths=local*rng.uniform(.08,.35,4);signs=rng.choice([-1,1],4);q0=np.poly(centers+signs*widths);r0=np.poly(centers-signs*widths);Q=np.polymul(q0,r0);cr=np.roots(np.polyder(Q));
 if max(abs(cr.imag))>1e-8:continue
 H=rng.uniform(.1,.85)*min(abs(np.polyval(Q,cr.real)));Pm=Q.copy();Pm[-1]-=H;Pp=Q.copy();Pp[-1]+=H;xx=np.roots(Pm);bb=np.roots(Pp)
 if max(abs(xx.imag))>1e-8 or max(abs(bb.imag))>1e-8:continue
 x8=np.sort(xx.real);betall=np.sort(bb.real);bet=betall[[0,1,4,5,6,7]];x=x8[inds];P=np.poly(x);den=np.polyval(np.polyder(P),x);f=np.vander(x,4,increasing=True);a=x8[5];b=x8[6];hf=float(gi)
 for bits0 in [None]:
  bits=(gi,);q=q0;r=r0;qv=np.polyval(q,x);rv=np.polyval(r,x);dw=-rv/den
  def maps(u):
   w=rv*(x-u)/den;G=f.T@(w[:,None]*f);Gp=f.T@((w*qv*qv/H)[:,None]*f);dr=-np.linalg.solve(Gp,G);DQ=rv[:,None]*f+qv[:,None]*(f@dr);dh=w@DQ;E=DQ-dh;AA=2*(dw@(w[:,None]*E))/(H*(dw@dw));B=.25*np.linalg.solve(G,f.T@(qv*dw*dw/w));return -np.outer(B,AA)
  eps=1e-7*(b-a);sol=solve_ivp(lambda u,z:(maps(u)@z.reshape(4,4)).ravel(),[a+eps,b-eps],np.eye(4).ravel(),rtol=2e-9,atol=1e-11);S=sol.y[:,-1].reshape(4,4);Si=np.linalg.inv(S)
  def vertex(u,missing):
   w=rv*(x-u)/den;keep=w>1e-8;xx=x[keep];ww=w[keep];ff=f[keep];qq=qv[keep];rr=rv[keep];G=ff.T@(ww[:,None]*ff);Gp=ff.T@((ww*qq*qq/H)[:,None]*ff);dr=-np.linalg.solve(Gp,G);DQ=rr[:,None]*ff+qq[:,None]*(ff@dr);dh=ww@DQ;fb=np.vander(bet,4,increasing=True);qb=np.polyval(q,bet);rb=np.polyval(r,bet);arows=(rb[:,None]*fb+qb[:,None]*(fb@dr)+dh)/H;Cs=4*np.linalg.solve(G,(qb[:,None]*fb).T);Rs=[np.eye(4)-2*np.outer(Cs[:,j],arows[j])/(arows[j]@Cs[:,j])for j in range(len(bet))];fg=np.array([1,missing,missing**2,missing**3]);edge=2*(np.polyval(r,missing)*fg+np.polyval(q,missing)*(fg@dr)-dh)/H
   return Rs,arows,edge,-dh
  RA,arA,edA,dA=vertex(a,a);RB,arB,edB,dB=vertex(b,b)
  if hf==.04 and bits==(0,0,0,0):print('TRACE edgeA',edA,'edgeB',edB,'refchangesA',[np.linalg.norm(edA@R-edA) for R in RA],flush=True)
  from scipy.optimize import linprog
  def feasible(rows):
   rows=np.array(rows);rows/=np.linalg.norm(rows,axis=1)[:,None];res=linprog([0,0,0,0,-1],A_ub=np.column_stack([-rows,np.ones(len(rows))]),b_ub=np.zeros(len(rows)),bounds=[(-1,1)]*4+[(0,1)],method='highs');return res.success and res.x[-1]>1e-7
  def words(Rs,ars,ed,dd):
   out=[];todo=[((),np.eye(4),[-ed,dd])]
   while todo:
    word,T,rows=todo.pop()
    if len(word)>=4:continue
    for j,R in enumerate(Rs):
     if word and word[-1]==j:continue
     T1=R@T;rows1=rows+[-ars[j]@T,dd@T1]
     if not feasible(rows1):continue
     if feasible(rows1+[ed@T1]):out.append((word+(j,),T1,np.array(rows1+[ed@T1])))
     if feasible(rows1+[-ed@T1]):todo.append((word+(j,),T1,rows1+[-ed@T1]))
   return out
  WA=words(RA,arA,edA,dA);WB=words(RB,arB,edB,dB);print('WORDS',len(WA),len(WB),flush=True)
  for ia,(wa,TA,ca) in enumerate(WA):
   for wb,TB,cb in WB:
    M=TA@Si@TB@S;ev,V=np.linalg.eig(M);constraints=np.vstack([cb@S,ca@Si@TB@S,edA])
    constraints/=np.linalg.norm(constraints,axis=1)[:,None]
    for z,vv in zip(ev,V.T):
     if abs(z.imag)>1e-7 or not 1e-4<z.real<.99999 or max(abs(vv.imag))>1e-7:continue
     for sg in [1,-1]:
      v=sg*vv.real;conds=constraints@v
      if min(conds)>1e-7:
       rec={'hf':hf,'bits':bits,'wa':wa,'wb':wb,'beta':bet.tolist(),'mu':z.real,'v':v.tolist(),'q':q.tolist(),'r':r.tolist(),'H':H,'S':S.tolist(),'conds':conds.tolist()};records.append(rec);print('CAND',len(records),hf,bits,wa,wb,'mu',z.real,flush=True)
json.dump(records,open('workspace/agent4_reflection_edge_cycles.json','w'));print('TOTAL',len(records))
