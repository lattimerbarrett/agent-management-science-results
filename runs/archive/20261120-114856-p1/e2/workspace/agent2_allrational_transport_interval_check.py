from sage.all import *
import pickle,time
from pathlib import Path
S,PX,p,q,h,left,right,eta,chi5,chi6,H,c,C,bb=pickle.load(open('workspace/agent2_rational_transport_setup.pkl','rb'));t=S.gen();RP=RealIntervalField(160);PS=PowerSeriesRing(RP,'e',default_prec=17);e=PS.gen();order=16
cof=H.adjugate()*vector(S.fraction_field(),[1,t,t*t]);nums=[S(cof[i]*q(t))for i in range(3)];ff=S((chi6/(PX.gen()-left)/(PX.gen()-right)/(PX.gen()-eta))(t));const=RP(h/(4*C*q(left)))
def peval(pol,x):
 ans=PS(0)
 for cc in pol.list()[::-1]:ans=ans*x+RP(cc)
 return ans
def pinv(q):
 aa=[1/q[0]]
 for n in range(1,17):aa.append(-sum(q[j]*aa[n-j]for j in range(1,n+1))/q[0])
 return PS(aa)+O(e**17)
def psqrt(q):
 aa=[q[0].sqrt()]
 for n in range(1,17):aa.append((q[n]-sum(aa[j]*aa[n-j]for j in range(1,n)))/(2*aa[0]))
 return PS(aa)+O(e**17)
def funcs(tt):
 den=(tt-RP(left))*(tt-RP(right))*(tt-RP(eta))*peval(ff,tt)+RP(h)
 ii=pinv(den);z=psqrt(RP(h)*ii)
 return [const*peval(pol,tt)*ii*z for pol in nums]
N=8192;out=[RP(0)for _ in range(3)];start=time.time()
for k in range(N):
 lo=left+(right-left)*k/N;hi=left+(right-left)*(k+1)/N;cc=(lo+hi)/2;hh=(hi-lo)/2
 point=funcs(PS(RP(cc))+e);bound=funcs(PS(RP(lo,hi))+e)
 for j in range(3):
  pol=sum(point[j][r]*RP(2*hh**(r+1)/(r+1))for r in range(0,16,2));err=max(abs(bound[j][16].lower()),abs(bound[j][16].upper()))*RP(2*hh**17/17)
  out[j]+=pol+RP(-err.upper(),err.upper())
 if k%2048==0:print(k,time.time()-start,flush=True)
U=identity_matrix(RP,3)+vector(RP,out).column()*vector(RP,c).row();print('u',out);print('U',U);print('widths',[[U[i,j].absolute_diameter()for j in range(3)]for i in range(3)]);print('time',time.time()-start)
with open('workspace/agent2_allrational_transport_intervals.pkl','wb')as f:pickle.dump((RP,out,U),f)
