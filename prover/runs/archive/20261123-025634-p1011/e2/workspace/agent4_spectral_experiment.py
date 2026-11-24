# Exploratory, non-certified inverse-DtN quadratic form.
# Not a proof of the target threshold: center Hessian/gluing are absent.
import numpy as np
from scipy.special import roots_jacobi,eval_jacobi,gammaln

def gram(n,l=2,J=1,Q=300,N=800):
 m=n-1;alpha=(m-2)/2+l
 t,w=roots_jacobi(N,alpha,alpha)
 r2=(1-t)/(1+t)
 gs=[]
 for j in range(J+1):
  if j==0:g=2*(1-l)/(1+t)**l
  else:g=(2*(1-l-2*j)*r2**j+4*j*(2*l+m+2*j-2)/m*r2**(j-1)/(1+t))/(1+t)**l
  gs.append(g)
 gs=np.array(gs);G=np.zeros((J+1,J+1))
 for q in range(Q):
  logh=(2*alpha+1)*np.log(2)-np.log(2*q+2*alpha+1)+2*gammaln(q+alpha+1)-gammaln(q+1)-gammaln(q+2*alpha+1)
  basis=eval_jacobi(q,alpha,alpha,t)*np.exp(-logh/2)
  coeff=(gs*w)@basis;k=l+q
  D=2*np.exp(gammaln((k+n+1)/2)+gammaln(k/2)-gammaln((k+n)/2)-gammaln((k-1)/2))
  G+=np.outer(coeff,coeff)/D
 return G

if __name__=='__main__':
 for J in [1,2,3,4]:
  print('J=',J)
  for n in range(max(12,4*J+7),36):
   G=gram(n,J=J,Q=250,N=700)
   d=np.sqrt(np.diag(G));G=G/d[:,None]/d[None,:]
   ii=np.arange(J+1);A=G*(ii[:,None]+ii[None,:]+1)
   print(n,np.linalg.eigvalsh(A)[0])
