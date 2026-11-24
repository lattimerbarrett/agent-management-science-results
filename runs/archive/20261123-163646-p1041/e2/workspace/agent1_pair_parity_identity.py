"""Check the proved pair-parity affine-function identity using exact FWHT."""
import numpy as np

def mobius(a):
 a=a.copy();m=len(a).bit_length()-1
 for i in range(m):
  b=a.reshape(-1,1<<(i+1));b[:,1<<i:]^=b[:,:1<<i]
 return a

def fwht(a):
 a=np.array(a,dtype=np.int64,copy=True);m=len(a).bit_length()-1
 for i in range(m):
  b=a.reshape(-1,1<<(i+1));x=b[:,:1<<i].copy();y=b[:,1<<i:].copy()
  b[:,:1<<i]=x+y;b[:,1<<i:]=x-y
 return a

def pair_parity(f):
 n=len(f);w=int(np.sum(f));assert w%2==0
 F=fwht(f);A=fwht(F*F)
 assert np.all(A%n==0)
 A//=n
 assert A[0]==w and np.all(A[1:]%2==0)
 Q=((A//2)%2).astype(np.uint8)
 Q[0]=(w//2)%2
 return Q

def run():
 rng=np.random.default_rng(275);count=0
 for m,r in [(4,2),(6,3),(9,5),(14,7),(15,8)]:
  t=m-r-1;bound=m-2*t-2
  deg=np.array([x.bit_count() for x in range(1<<m)])
  for j in range(40):
   coeff=rng.integers(0,2,size=1<<m,dtype=np.uint8);coeff[deg>r]=0
   f=mobius(coeff);Q=pair_parity(f);aq=mobius(Q)
   assert np.all(aq[deg>bound]==0)
   if bound==0:assert np.all(Q==((int(f.sum())//2)%2))
   count+=1
 print('Pair-parity degree identity checked on',count,'independent random RM codewords, including m14 and15.')

if __name__=='__main__':run()
