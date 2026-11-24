from sage.all import *
import pickle,time
R=RealIntervalField(100);S=PowerSeriesRing(R,'e',default_prec=9);e=S.gen();d=R(35).sqrt()
def psqrt(q):
 aa=[q[0].sqrt()]
 for n in range(1,9):aa.append((q[n]-sum(aa[j]*aa[n-j]for j in range(1,n)))/(2*aa[0]))
 return S(aa)+O(e**9)
def pinv(q):
 aa=[1/q[0]]
 for n in range(1,9):aa.append(-sum(q[j]*aa[n-j]for j in range(1,n+1))/q[0])
 return S(aa)+O(e**9)
def funcs(tt):
 f=tt**3-7*tt;den=(d+6)*(d-f)*(d+f);z=psqrt((d-f)*(d-6)*pinv((d+f)*(d+6)))
 N0=-3*tt**4-2*tt**3*d+6*tt**2*d+42*tt**2+6*tt*d+d*d-14*d-147
 N1=2*tt**4-8*tt**3+3*tt**2*d+14*tt**2-4*tt*d-3*d
 N2=-tt**4+4*tt**3+2*tt**2+2*tt*d-2*d-21
 ii=pinv(den)
 return [d*N0*ii*z,-d*N1*ii*z,-d*N2*ii*z]
N=2048;out=[R(0)for _ in range(3)];start=time.time()
for k in range(N):
 lo=QQ(1)+QQ(k)/N;hi=QQ(1)+QQ(k+1)/N;c=(lo+hi)/2;hh=(hi-lo)/2
 try:
  ff=funcs(S(R(c))+e);bounds=funcs(S(R(lo,hi))+e)
 except Exception:
  print('FAILED k',k,'I',R(lo,hi),'d',d,'finterval',R(lo,hi)**3-7*R(lo,hi),flush=True);raise
 for j in range(3):
  pol=sum(ff[j][r]*R(2*hh**(r+1)/(r+1))for r in [0,2,4,6]);err=bounds[j][8].absolute_diameter() if False else max(abs(bounds[j][8].lower()),abs(bounds[j][8].upper()))*R(2*hh**9/9)
  out[j]+=pol+R(-err.upper(),err.upper())
 if k%128==0:print(k,'time',time.time()-start,flush=True)
print('uintervals',out,'time',time.time()-start)
print('identity u1+2u2',out[1]+2*out[2])
with open('workspace/agent2_h1_transport_intervals.pkl','wb')as f:pickle.dump((R,out),f)
