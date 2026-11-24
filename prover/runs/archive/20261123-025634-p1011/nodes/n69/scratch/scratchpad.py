import os
print('EXPERIMENTS',os.listdir('experiments'))
for ex in ['e1','e3','e5']:
 print(ex, os.listdir('experiments/'+ex))
 for p in os.listdir('experiments/'+ex):
  print(p, os.path.isdir('experiments/'+ex+'/'+p), os.path.islink('experiments/'+ex+'/'+p))
for root,dirs,files in os.walk('experiments'):
 if any(('certificate' in f or 'high_dim_analytic' in f or 'local_pohozaev' in f or 'spectral_full' in f) for f in files):
  print(root,[f for f in files if 'certificate' in f or 'high_dim_analytic' in f or 'local_pohozaev' in f or 'spectral_full' in f])
import numpy as np
from scipy.special import gammaln, betaln

def mat(n,N=200000):
 a=(n+2)/2
 p=np.arange(N,dtype=float); L=p+2
 logq=np.log(2*(L-1)*(L+n-1))+gammaln((L+1)/2)+gammaln((L+n)/2)-gammaln((L+n-1)/2)-gammaln(L/2)
 lognorm=np.log(np.pi)+(1-2*a)*np.log(2)+gammaln(p+2*a)-gammaln(p+1)-np.log(p+a)-2*gammaln(a)
 vals=[]
 for s in (1,2):
  li=(2*a-s)*np.log(2)+betaln(a+.5-s,a+.5)+gammaln(p+2*a)-gammaln(2*a)-gammaln(p+1)+gammaln(p+s)-gammaln(s)-gammaln(p+2*a+1-s)+gammaln(2*a+1-s)
  vals.append(np.exp(li+(logq-lognorm)/2))
 v0=vals[0]/2; v1=vals[1]-vals[0]/2
 A=v0@v0; B=v0@v1; C=v1@v1
 return A,B,C,B*B/(A*C)
from math import comb

def genmat(n,k,N=100000):
 a=(n+2)/2
 p=np.arange(N,dtype=float); L=p+2
 logq=np.log(2*(L-1)*(L+n-1))+gammaln((L+1)/2)+gammaln((L+n)/2)-gammaln((L+n-1)/2)-gammaln(L/2)
 lognorm=np.log(np.pi)+(1-2*a)*np.log(2)+gammaln(p+2*a)-gammaln(p+1)-np.log(p+a)-2*gammaln(a)
 vals=[]
 for s in range(1,k+2):
  li=(2*a-s)*np.log(2)+betaln(a+.5-s,a+.5)+gammaln(p+2*a)-gammaln(2*a)-gammaln(p+1)+gammaln(p+s)-gammaln(s)-gammaln(p+2*a+1-s)+gammaln(2*a+1-s)
  vals.append(np.exp(li+(logq-lognorm)/2))
 vs=[]
 for j in range(k+1):
  vs.append(sum(comb(j,s-1)*2**(s-1)*(-1)**(j+1-s)*vals[s-1]/2 for s in range(1,j+2)))
 vs=np.array(vs)
 A=vs@vs.T
 D=(2+2*np.arange(k+1)[:,None]+2*np.arange(k+1)[None,:])*A
 D=D/np.sqrt(np.diag(D)[:,None]*np.diag(D)[None,:])
 return np.linalg.eigvalsh(D),A
def angularmat(n,l,k,N=10000):
 a=l+(n-2)/2
 p=np.arange(N,dtype=float); L=p+l
 good=L>=2
 q=np.zeros(N)
 Lg=L[good]
 q[good]=np.exp(np.log(2*(Lg-1)*(Lg+n-1))+gammaln((Lg+1)/2)+gammaln((Lg+n)/2)-gammaln((Lg+n-1)/2)-gammaln(Lg/2))
 lognorm=np.log(np.pi)+(1-2*a)*np.log(2)+gammaln(p+2*a)-gammaln(p+1)-np.log(p+a)-2*gammaln(a)
 vals={}
 for s in range(max(1,l-1),l+k):
  li=(2*a-s)*np.log(2)+betaln(a+.5-s,a+.5)+gammaln(p+2*a)-gammaln(2*a)-gammaln(p+1)+gammaln(p+s)-gammaln(s)-gammaln(p+2*a+1-s)+gammaln(2*a+1-s)
  vals[s]=np.exp(li-lognorm/2)*np.sqrt(q)
 vs=[]
 for j in range(k+1):
  vs.append(sum((comb(j,r)*2**r*(-1)**(j-r)*vals[l-1+r]/2 for r in range(j+1) if l-1+r in vals),np.zeros(N)))
 vs=np.array(vs)
 return vs@vs.T

for n in [19,21,25]:
 K=(n-5)//4
 A=angularmat(n,2,K)
 A1=angularmat(n,1,K)
 A3=angularmat(n,3,K-1)
 js=np.arange(K+1)
 D=(2+2*js[:,None]+2*js[None,:])*A
 norm=np.sqrt(np.diag(D)); Dn=D/norm[:,None]/norm[None,:]
 ee,vv=np.linalg.eigh(Dn)
 c=vv[:,0]/norm
 # root of derivative of q(eps), using t=eps**2
 poly=np.zeros(2*K+2)
 for i in range(K+1):
  for j in range(K+1):poly[i+j]+= (i+j+1)*A[i,j]*c[i]*c[j]
 roots=np.roots(np.trim_zeros(poly,'b')[::-1])
 out=[]
 for r in roots:
  if abs(r.imag)>1e-6 or r.real<=0:continue
  t=r.real
  cc=c*t**js
  scale2=sum((i+j)*(i+j+1)*A[i,j]*cc[i]*cc[j] for i in range(K+1) for j in range(K+1))
  b=(2+4*js/(n+1))*cc
  d=2*js[1:]*cc[1:]
  dd=np.zeros(K+1); dd[:-1]=2*js[1:]*(n+1+2*js[1:])*cc[1:]
  tang=(n+1)/2*(b@A1@b)+(n-1)/(n+1)*(d@A3@d)+(cc@A@dd)
  hs=[]
  m=n-1
  for s in [(m-1)/m,1/(m*(m-1)),1/m]:
   r1=s*(m+2)/2
   r3=1/(m+4)+2*m*s/((m+2)*(m+4))
   e=np.zeros(K+1)
   e[:-1]=((2+8*s)*js[1:]+4*(1+4*s)/(m+4)*(js[1:]-1)*js[1:])*cc[1:]
   hs.append(r1*(b@A1@b)+r3*(d@A3@d)+cc@A@e)
  out.append((round(t,4),round(scale2,6),round(tang,6),hs))
 print(n,ee[0],out)
