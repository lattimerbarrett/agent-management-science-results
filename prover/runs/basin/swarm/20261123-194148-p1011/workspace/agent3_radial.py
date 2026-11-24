exec(open('workspace/agent3_translation.py').read().split('n=19;m=n-1;')[0])
for ell in [1]:
 for d in range(2,6):
  first=None
  for n in range(2*ell+4*d+1,80):
   C=Cmat(n,ell,d,10000)[1:,1:];scale=np.sqrt(np.diag(C)); C/=scale[:,None]*scale[None,:]
   qs=np.arange(1,d+1);D=(2*ell-2+2*qs[:,None]+2*qs[None,:])*C
   if np.linalg.eigvalsh(D)[0]<-1e-7: first=n;break
  print('ell1 d',d,'first',first)

def C0(n,d,N=20000):
 ell=0;pbase=1; a=(n-3)/2;alpha=a+.5;js=np.arange(2,N,dtype=float)
 logI0=(2*a-pbase+1)*np.log(2)+betaln(a+1,a-pbase+1)
 logI=logI0+gammaln(js+pbase)-gammaln(pbase)-gammaln(js+1)+gammaln(js+2*a+1)-gammaln(2*a+1)+gammaln(2*a-pbase+2)-gammaln(js+2*a-pbase+2)
 logh=np.log(np.pi)+(1-2*alpha)*np.log(2)+gammaln(js+2*alpha)-gammaln(js+1)-np.log(js+alpha)-2*gammaln(alpha)
 k=js
 logb=np.log(2)+gammaln((k+n+1)/2)+gammaln(k/2)-gammaln((k+n)/2)-gammaln((k-1)/2)
 w=np.exp(2*logI-logh-logb)
 ratios=[np.ones_like(js)]
 for p in range(1,d):ratios.append(ratios[-1]*(js+p)*(2*a-p+1+js)/(p*2*(a-p)))
 gs=[]
 for q in range(2,d+1):
  c=q*(2*q+n-3)/(n-1);vec=np.zeros_like(js)
  for e,coef in [(q-1,c),(q,c+1-2*q)]:
   for p in range(1,e+1):vec+=coef*comb(e,p)*2**p*(-1)**(e-p)*ratios[p-1]
  gs.append(vec)
 return (np.array(gs)*w)@np.array(gs).T
for d in range(3,7):
 first=None
 for n in range(4*d+1,90):
  C=C0(n,d);scale=np.sqrt(np.diag(C));C/=scale[:,None]*scale[None,:]
  qs=np.arange(2,d+1);D=(-2+2*qs[:,None]+2*qs[None,:])*C
  if np.linalg.eigvalsh(D)[0]<-1e-7:first=n;break
 print('ell0 d',d,'first',first)
