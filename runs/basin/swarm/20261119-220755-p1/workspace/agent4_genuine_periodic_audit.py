"""Independent high-precision checks of genuine s4 periodic candidate and map.
Numerical checks, not the interval existence certificate.
"""
import numpy as np,mpmath as mp,sys
from scipy.interpolate import CubicSpline
sys.path.insert(0,'workspace')
from agent2_blowup_ode import BlowupODE
D=np.load('workspace/agent1_GENUINE_s4_periodic.npz');S=D['base'];f=D['f'];g=D['g'];N=float(D['L']);mus=D['mus'];Y=D['y'];T=float(D['p'][0])
ob=BlowupODE(S,f,g,N,mus)
Ds=[];mins=[];maxfield=0
for yy in Y.T:
 H=S+yy[0];p=N*H/(ob.d*ob.fv)
 Ds.append(N*np.dot(p,(ob.V@yy[1:5])/ob.fv));mins.append(min(p))
assert min(mins)>0 and max(Ds)<0
print('theta range',-Y[0].max(),-Y[0].min(),'minimum Z',min(Y[-2:].ravel()))
print('minimum base probability',min(mins),'deltaN range',min(Ds),max(Ds))
assert np.linalg.norm(Y[:,0]-Y[:,-1])<1e-10
# Check the differential residual independently, using a spline derivative.
cs=CubicSpline(D['x'],D['a'],axis=1,bc_type='periodic')
xs=(D['x'][:-1]+D['x'][1:])/2
errs=[]
for xx in xs[::4]:
 aa=cs(xx);yy=aa.copy();th=1/(1+np.exp(-aa[0]));yy[0]=-th;yy[-2:]=np.exp(aa[-2:])
 ff=ob(0,yy,True);ff[0]=-ff[0]/(th*(1-th));ff[-2:]/=yy[-2:]
 errs.append(np.linalg.norm(cs(xx,1)-T*ff))
print('Independent spline ODE residual max',max(errs))
assert max(errs)<.001
mp.mp.dps=70
SS=list(map(mp.mpf,S));NN=mp.mpf(3)/50;q1=-mp.mpf(289)/400;q2=mp.mpf(17)/10
P=lambda z:mp.fprod(z-a for a in SS)*(z-q1)*(z-q2)
rt=np.sort(np.roots(np.polymul(np.poly(S),np.poly([float(q1),float(q2)]))+np.r_[np.zeros(8),N]))
roots=[mp.findroot(lambda z:P(z)+NN,mp.mpf(float(r))) for r in rt]
assert max(abs(P(r)+NN) for r in roots)<mp.mpf('1e-60')
def pmul(a,b):
 c=[mp.mpf(0)]*(len(a)+len(b)-1)
 for i,aa in enumerate(a):
  for j,bb in enumerate(b):c[i+j]+=aa*bb
 return c
def fromroots(rr):
 c=[mp.mpf(1)]
 for r in rr:c=pmul(c,[-r,1])
 return c
ff=fromroots([roots[i] for i in [0,3,5,6]]);gg=fromroots([roots[i] for i in [1,2,4,7]])
mm=[mp.findroot(lambda z:P(z)+2*NN,mp.mpf(float(r))) for r in mus]
val=lambda c,z:mp.polyval(c[::-1],z)
dd=[mp.fprod(a-b for b in SS if a!=b) for a in SS]
VV=mp.matrix([[a**j for j in range(4)] for a in SS]);VM=mp.matrix([[a**j for j in range(4)] for a in mm])
FV=[val(ff,a) for a in SS];GV=[val(gg,a) for a in SS];FM=[val(ff,a) for a in mm];GM=[val(gg,a) for a in mm]
def op(p,nodes):
 V=mp.matrix([[a**j for j in range(4)] for a in nodes]);M=V.T*mp.diag(p)*V
 c=mp.lu_solve(M,-V.T*mp.matrix([p[i]*a**4 for i,a in enumerate(nodes)]))
 fv=[a**4+sum(c[j]*a**j for j in range(4)) for a in nodes];norm=sum(p[i]*fv[i]**2 for i in range(len(p)))
 return list(c),norm,[p[i]*fv[i]**2/norm for i in range(len(p))]
def field(y):
 h=y[0];w=mp.matrix(y[1:5]);Z=y[-2:];H=[a+h for a in SS];wv=VV*w
 p=[NN*H[i]/dd[i]/FV[i] for i in range(6)];pp=[H[i]*FV[i]/dd[i] for i in range(6)]
 M=VV.T*mp.diag(p)*VV;Mp=VV.T*mp.diag(pp)*VV
 dg=mp.lu_solve(Mp,-M*w);dn=NN*sum(p[i]*wv[i]/FV[i] for i in range(6))
 dgv=VV*dg;ratio=[(GV[i]*wv[i]+FV[i]*dgv[i]-dn)/NN for i in range(6)]
 wf=mp.lu_solve(M,-VV.T*mp.matrix([p[i]*FV[i]*ratio[i]**2 for i in range(6)])-4*VM.T*mp.matrix([Z[i]*FM[i] for i in range(2)]))
 grow=[2+2*((VM*w)[i]/FM[i]+(VM*dg)[i]/GM[i])-2*dn/NN for i in range(2)]
 return mp.matrix([2*H[2]*ratio[2]]+list(w+wf)+[Z[i]*grow[i] for i in range(2)])
for j in np.linspace(0,Y.shape[1]-2,7,dtype=int):
 y=list(map(lambda z:mp.mpf(float(z)),Y[:,j]));v=field(y)
 assert max(abs(v[i]-mp.mpf(float(ob(0,np.array(list(map(float,y))),True)[i])) ) for i in range(7))<mp.mpf('1e-5')
 constants=[]
 for eps in map(mp.mpf,['.0004','.0002','.0001']):
  fe=[ff[i]+(eps*y[1+i] if i<4 else 0) for i in range(5)]
  base=[(SS[i]+y[0])/dd[i]/val(fe,SS[i]) for i in range(6)];base=[b/sum(base) for b in base]
  ext=[eps**2*z for z in y[-2:]];p=[b*(1-sum(ext)) for b in base]+ext
  ns=SS+mm;p2=op(op(p,ns)[2],ns)[2];bp=[a/sum(p2[:6]) for a in p2[:6]]
  fc,norm,_=op(bp,SS);hv=[dd[i]*bp[i]*(SS[i]**4+val(fc,SS[i]))/norm-SS[i] for i in range(6)]
  assert max(hv)-min(hv)<mp.mpf('1e-50')
  ep=eps/(1+eps);yp=mp.matrix([sum(hv)/6]+[(fc[i]-ff[i])/ep for i in range(4)]+[z/ep**2 for z in p2[6:]])
  rr=yp-mp.matrix(y)-eps*v;constants.append(float(mp.norm(rr)/eps**2))
 print('phase',float(D['x'][j]),'high-precision Taylor constants',constants)
 assert max(constants)<1e7 and abs(constants[-1]-constants[-2])<max(constants)*.1
print('All independent finite checks passed.')
