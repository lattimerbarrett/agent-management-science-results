import numpy as np,json
from pathlib import Path
rec=next(t for t in json.load(open('workspace/agent4_reflection_edge_cycles.json')) if t['hf']==26)
q=np.array(rec['q']);r=np.array(rec['r']);H=rec['H'];S=np.array(rec['S']);v=np.array(rec['v']);bet=np.array(rec['beta']);Q=np.polymul(q,r);Q[-1]-=H;xx=np.sort(np.roots(Q).real);inds=[0,1,4,5,6,7];x=xx[inds];P=np.poly(x);den=np.polyval(np.polyder(P),x);f=np.vander(x,4,increasing=True);qv=np.polyval(q,x);rv=np.polyval(r,x);a=xx[5];b=xx[6]
def vertex(u):
 w=rv*(x-u)/den;keep=w>1e-8;ff=f[keep];ww=w[keep];qq=qv[keep];rr=rv[keep];G=ff.T@(ww[:,None]*ff);Gp=ff.T@((ww*qq*qq/H)[:,None]*ff);dr=-np.linalg.solve(Gp,G);DQ=rr[:,None]*ff+qq[:,None]*(ff@dr);dh=ww@DQ;fb=np.vander(bet,4,increasing=True);qb=np.polyval(q,bet);rb=np.polyval(r,bet);ar=(rb[:,None]*fb+qb[:,None]*(fb@dr)+dh)/H;Cs=4*np.linalg.solve(G,(qb[:,None]*fb).T);Rs=[np.eye(4)-2*np.outer(Cs[:,j],ar[j])/(ar[j]@Cs[:,j])for j in range(len(bet))]
 def ghost(z):
  fg=np.array([1,z,z*z,z**3]);return 2*(np.polyval(r,z)*fg+np.polyval(q,z)*(fg@dr)-dh)/H
 return Rs,-2*ar,ghost,-dh
RA,ga,ghostA,dA=vertex(a);RB,gb,ghostB,dB=vertex(b);j=rec['wa'][0];k=rec['wb'][0];vinB=S@v;voutB=RB[k]@vinB;vinA=np.linalg.solve(S,voutB);voutA=RA[j]@vinA
print('xx',xx,'A/B',a,b,'checkmu',np.linalg.norm(voutA-rec['mu']*v))
ua=ga[j]@vinA;ub=gb[k]@vinB
rA=-(ghostA(a)@vinA)/(ghostA(a)@voutA);rB=-(ghostB(b)@vinB)/(ghostB(b)@voutB)
cAB=(ga[k]@vinA+rA*(ga[k]@voutA))/ua
cBA=(gb[j]@vinB+rB*(gb[j]@voutB))/ub
M=np.array([[rA+cBA*cAB,-cBA],[-rB*cAB,rB]])
print('rates ua ub',ua,ub,'rA rB',rA,rB,'cAB cBA',cAB,cBA,'M',M,'eig',np.linalg.eig(M))
print('otherghost integrated coeffA/B',[(z,(ghostA(z)@vinA+rA*ghostA(z)@voutA)/ua,(ghostB(z)@vinB+rB*ghostB(z)@voutB)/ub)for z in xx[[2,3]]])
Path('workspace/agent2_log_reflection_model26.py').write_text(Path('scratchpad.py').read_text().split("Path('workspace/agent2_log_reflection_model26.py')")[0])