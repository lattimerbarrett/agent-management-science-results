from sage.all import *
from agent4_interval_blowup import IntervalBlowup,Jet2
class BalancedField:
 def __init__(self,data,q1='-289/400',bits=300):
  self.ob=IntervalBlowup(q1=q1,bits=bits,kind='ball');self.K=self.ob.R;K=self.K
  self.S=matrix(K,[[K(float(v)) for v in row] for row in data['B']]);self.S[0,:]=-self.S[0,:];self.Si=self.S.inverse();self.bt=list(self.S.row(0));self.Bw=[list(self.S.row(i)) for i in range(1,5)];self.Bz=[list(self.S.row(i)) for i in range(5,7)];self.Iw=[[self.Si[i,j] for j in range(1,5)] for i in range(7)];self.Iz=[[self.Si[i,j] for j in range(5,7)] for i in range(7)];self.It=list(self.Si.column(0));self.E=[[sum(self.Iw[i][k]*self.Bw[k][j] for k in range(4))+2*sum(self.Iz[i][m]*self.Bz[m][j] for m in range(2)) for j in range(7)] for i in range(7)]
 def coeff(self,th,ref):
  co=self.ob.coefficient_formulas(th);b,K,F,L=co['b'],co['K'],co['force'],co['L'];w=ref[1:5];Z=ref[5:];v0=sum(b[k]*w[k] for k in range(4));vr=[sum(b[k]*self.Bw[k][j] for k in range(4)) for j in range(7)];lm0=[sum(L[m][k]*w[k] for k in range(4)) for m in range(2)];lm=[[sum(L[m][k]*self.Bw[k][j] for k in range(4)) for j in range(7)] for m in range(2)];kk=[sum(self.Iw[i][k]*K[k] for k in range(4)) for i in range(7)];ff=[[sum(self.Iw[i][k]*F[k][m] for k in range(4)) for m in range(2)] for i in range(7)];cc=[sum(self.Iw[i][k]*w[k] for k in range(4))+2*sum(self.Iz[i][m]*Z[m] for m in range(2))+self.It[i]*v0-kk[i]*v0*v0+sum(ff[i][m]*Z[m]+self.Iz[i][m]*Z[m]*lm0[m] for m in range(2)) for i in range(7)];AA=[[self.E[i][j]+self.It[i]*vr[j]-2*kk[i]*v0*vr[j]+sum(ff[i][m]*self.Bz[m][j]+self.Iz[i][m]*(Z[m]*lm[m][j]+lm0[m]*self.Bz[m][j]) for m in range(2)) for j in range(7)] for i in range(7)];return cc,AA,kk,vr,lm
 def fj(self,q,ref,wantjac=False):
  th=ref[0]+sum(self.bt[j]*q[j] for j in range(7));co=self.coeff(Jet2(th,th*0+1,th*0) if wantjac else th,ref)
  if wantjac:
   cc,AA,kk,vr,lm=co;ccp=[a.d for a in cc];AAp=[[a.d for a in row] for row in AA];kkp=[a.d for a in kk];vrp=[a.d for a in vr];lmp=[[a.d for a in row] for row in lm];cc=[a.v for a in cc];AA=[[a.v for a in row] for row in AA];kk=[a.v for a in kk];vr=[a.v for a in vr];lm=[[a.v for a in row] for row in lm]
  else:cc,AA,kk,vr,lm=co
  u=sum(vr[j]*q[j] for j in range(7));dd=[sum(self.Bz[m][j]*q[j] for j in range(7)) for m in range(2)];ee=[sum(lm[m][j]*q[j] for j in range(7)) for m in range(2)];ff=[cc[i]+sum(AA[i][j]*q[j] for j in range(7))-kk[i]*u*u+sum(self.Iz[i][m]*dd[m]*ee[m] for m in range(2)) for i in range(7)]
  if not wantjac:return ff
  up=sum(vrp[j]*q[j] for j in range(7));ep=[sum(lmp[m][j]*q[j] for j in range(7)) for m in range(2)];jj=[[AA[i][j]-2*kk[i]*u*vr[j]+sum(self.Iz[i][m]*(dd[m]*lm[m][j]+ee[m]*self.Bz[m][j]) for m in range(2))+self.bt[j]*(ccp[i]+sum(AAp[i][k]*q[k] for k in range(7))-kkp[i]*u*u-2*kk[i]*u*up+sum(self.Iz[i][m]*dd[m]*ep[m] for m in range(2))) for j in range(7)] for i in range(7)];return ff,jj
 def jets(self,ref,order=20,q0=None,variational=False):
  R=PowerSeriesRing(self.K,'t',default_prec=order+1);t=R.gen();q=[R(0) for _ in range(7)] if q0 is None else [R(v) for v in q0];mm=identity_matrix(R,7)
  for j in range(order):
   if variational:
    ff,jj=self.fj(q,ref,True);df=matrix(R,jj)*mm;mm+=matrix(R,7,7,lambda a,b:df[a,b][j]*t**(j+1)/(j+1))
   else:ff=self.fj(q,ref)
   q=[q[i]+ff[i][j]*t**(j+1)/(j+1) for i in range(7)]
  return (q,mm) if variational else q
