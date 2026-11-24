import numpy as np
from scipy.special import gammaln, betaln

def gram(n,K=10000):
 m=n-1; al=(m+3)/2
 k=np.arange(K,dtype=float); l=k+2
 logh=(np.log(np.pi)+(1-2*al)*np.log(2)+gammaln(k+2*al)-gammaln(k+1)-np.log(k+al)-2*gammaln(al))
 def moment(p):
  return np.exp((2*al-p)*np.log(2)+betaln(al+.5-p,al+.5)+gammaln(k+2*al)-gammaln(2*al)-gammaln(k+1)+gammaln(k+p)-gammaln(p)+gammaln(2*al+1-p)-gammaln(k+2*al+1-p)-.5*logh)
 a=moment(1)/2; b=moment(2)-a
 T=2*np.exp(gammaln((l+n+1)/2)+gammaln(l/2)-gammaln((l-1)/2)-gammaln((l+n)/2))
 q=((l-1)*(l+m))**2/T
 A=np.dot(q*a,a);B=np.dot(q*a,b);C=np.dot(q*b,b)
 return B*B/(A*C), (A,B,C)
from math import comb

def matrix(n,h,K=5000):
 m=n-1; al=h+(m-1)/2
 i0=max(0,2-h) if h<2 else 0
 imax=(n-1-2*h)//4
 if imax<i0:return None
 k=np.arange(K,dtype=float); l=k+h
 logh=np.log(np.pi)+(1-2*al)*np.log(2)+gammaln(k+2*al)-gammaln(k+1)-np.log(k+al)-2*gammaln(al)
 def moment(p):
  if p<=0: return np.zeros(K)
  return np.exp((2*al-p)*np.log(2)+betaln(al+.5-p,al+.5)+gammaln(k+2*al)-gammaln(2*al)-gammaln(k+1)+gammaln(k+p)-gammaln(p)+gammaln(2*al+1-p)-gammaln(k+2*al+1-p)-.5*logh)
 vs=[]; ds=[]
 for i in range(i0,imax+1):
  v=sum(comb(i,j)*2**(i-j)*(-1)**j*moment(h+i-1-j)/2 for j in range(i+1))
  vs.append(v);ds.append(h+2*i-1)
 T=2*np.exp(gammaln((l+n+1)/2)+gammaln(l/2)-gammaln((l-1)/2)-gammaln((l+n)/2))
 with np.errstate(invalid='ignore',divide='ignore'):
  q=((l-1)*(l+m))**2/T
 q[l<2]=0
 vs=np.array(vs);G=(vs*q)@vs.T
 ds=np.array(ds);H=(ds[:,None]+ds[None,:])*G
 diag=np.sqrt(np.diag(H));H/=diag[:,None]*diag[None,:]
 return np.linalg.eigvalsh(H)[0], len(ds)
def rawgram(n,h,imin,imax,K=20000):
 m=n-1; al=h+(m-1)/2
 k=np.arange(K,dtype=float); l=k+h
 logh=np.log(np.pi)+(1-2*al)*np.log(2)+gammaln(k+2*al)-gammaln(k+1)-np.log(k+al)-2*gammaln(al)
 def moment(p):
  if p<=0:return np.zeros(K)
  return np.exp((2*al-p)*np.log(2)+betaln(al+.5-p,al+.5)+gammaln(k+2*al)-gammaln(2*al)-gammaln(k+1)+gammaln(k+p)-gammaln(p)+gammaln(2*al+1-p)-gammaln(k+2*al+1-p)-.5*logh)
 vs=[]
 for i in range(imin,imax+1):
  vs.append(sum(comb(i,j)*2**(i-j)*(-1)**j*moment(h+i-1-j)/2 for j in range(i+1)))
 T=2*np.exp(gammaln((l+n+1)/2)+gammaln(l/2)-gammaln((l-1)/2)-gammaln((l+n)/2))
 with np.errstate(invalid='ignore',divide='ignore'):
  q=((l-1)*(l+m))**2/T
 q[l<2]=0
 vs=np.array(vs)
 return (vs*q)@vs.T

if __name__=='__main__' and False:
 from scipy.optimize import brentq
 n=19;m=n-1
 G=rawgram(n,2,0,3)
 d=1+2*np.arange(4)
 H=(d[:,None]+d[None,:])*G
 scale=np.sqrt(np.diag(H))
 eig,vec=np.linalg.eigh(H/scale[:,None]/scale[None,:])
 a=vec[:,0]/scale;a/=a[0]
 def deriv(lam):
  b=a*lam**d
  return b@H@b
 roots=[]
 xx=np.geomspace(.01,100,1000)
 for x,y in zip(xx[:-1],xx[1:]):
  if deriv(x)*deriv(y)<0:roots.append(brentq(deriv,x,y))
 print('a',a, 'eigen',eig,'roots',roots)
 G1=rawgram(n,1,0,3)
 G3=rawgram(n,3,0,2)
 for lam in roots:
  b=a*lam**d
  radial2=b@((d[:,None]+d[None,:])**2*G)@b
  print('root',lam,'scale second norm',radial2)
  for r in [0,1/m,.5]:
   i=np.arange(4);cc=1+2*i/(m+2)
   s1=2*(m+2)*r*((b*cc)@G1@(b*cc))
   s3=(1/(m+4)+2*m*r/((m+2)*(m+4)))*((2*i[1:]*b[1:])@G3@(2*i[1:]*b[1:]))
   dj=2*i+8*i*r+4*i*(i-1)/(m+4)*(1+4*r)
   s2=sum(b[j]*dj[j]*np.dot(b,G[:,j-1]) for j in range(1,4))
   print('translation',r, 2*(s1+s2+s3), 'terms',s1,s2,s3)

# A rational certificate for the sign-changing dilation quadratic form
# in ambient dimension 19. No floating point is used in the certificate.
if __name__=='__main__':
 from gmpy2 import mpq
 from math import factorial, prod
 Q=mpq
 n=19; K=300
 a=[Q(1),Q(-461,1000),Q(56,1000),Q(-1386,1000000)]
 d=[1,3,5,7]
 def moment_polynomial_coefficients(a):
  out={p:Q(0) for p in range(1,5)}
  for i,ai in enumerate(a):
   for j in range(i+1):
    p=1+i-j
    out[p]+=ai*comb(i,j)*2**(i-j)*(-1)**j/2
  return out
 A=moment_polynomial_coefficients(a)
 B=moment_polynomial_coefficients([ai*di for ai,di in zip(a,d)])
 C={p:Q(2**(21-p)*factorial(10-p)*factorial(10),factorial(20)*factorial(p-1)) for p in range(1,5)}
 Ch=Q(2**20*factorial(10)**2,factorial(20)**2)
 def Ip(k,p):
  return C[p]*prod(k+j for j in range(1,p))*prod(k+j for j in range(22-p,21))
 def h(k):return Ch*prod(k+j for j in range(1,21))/Q(2*k+21,2)
 # q_2/pi and q_3*pi, respectively.
 qe=Q(20**2*factorial(0)*factorial(20),2*4**10*factorial(10)**2)
 qo=Q(2**2*21**2*4**12*factorial(11)*factorial(1)*factorial(0)*factorial(10),2*factorial(22)*factorial(2))
 sums=[Q(0),Q(0)]
 for k in range(K):
  l=k+2
  x=sum(A[p]*Ip(k,p) for p in A)
  y=sum(B[p]*Ip(k,p) for p in B)
  q=qe if k%2==0 else qo
  sums[k%2]+=2*q*x*y/h(k)
  ratio=Q((l+1)**2*(l+20)*(l+19),(l-1)*l*(l+18)**2)
  if k%2==0:qe*=ratio
  else:qo*=ratio
 # Machin's formula, with alternating-series bounds, certifies pi.
 def atan_bounds(q,terms):
  s=sum(Q((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(terms))
  t=Q((-1)**terms,(2*terms+1)*q**(2*terms+1))
  return min(s,s+t),max(s,s+t)
 a0,a1=atan_bounds(5,35);b0,b1=atan_bounds(239,10)
 plo,phi=16*a0-4*b1,16*a1-4*b0
 def interval_times(c,lo,hi):return (c*lo,c*hi) if c>=0 else (c*hi,c*lo)
 lo0,hi0=interval_times(sums[0],plo,phi)
 lo1,hi1=interval_times(sums[1],1/phi,1/plo)
 def M(coeff):
  return sum(abs(coeff[p])*C[p]*(1+Q(20,K))**(2*p-2)*Q(1,K**(8-2*p)) for p in coeff)
 tail=2*M(A)*M(B)/Ch*(1+Q(20,K))**3*(1+Q(21,2*K))*Q(1,3*(K-1)**3)
 lower=lo0+lo1-tail;upper=hi0+hi1+tail
 print('Certified interval for the dilation quadratic form:')
 print(float(lower),float(upper))
 print('Certified absolute tail bound:',float(tail))
 assert upper<0
 print('EXACT RATIONAL SIGN CERTIFICATE PASSED')
 from scipy.optimize import brentq
 G=rawgram(19,2,0,3)
 da=np.array([float(x) for x in a]);dd=np.array(d)
 H=(dd[:,None]+dd[None,:])*G
 def fun(lam):
  av=da*lam**dd
  return av@H@av
 root=brentq(fun,.8,1)
 print('Exploratory root, not a certificate:',root, 'derivative endpoints',fun(.95),fun(.96))
