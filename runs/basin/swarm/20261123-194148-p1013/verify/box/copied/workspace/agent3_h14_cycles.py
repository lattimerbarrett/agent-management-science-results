import math,sys
from fractions import Fraction
sys.path.insert(0,'workspace')
from agent2_cycles import matching_both,brute

def a_components_cycles(a,b,ntri,nmatch):
 assert 3*ntri+2*nmatch<=a
 pol={(0,0):1}
 for opts in ([[(0,0,1),(1,1,3),(2,1,3)]]*ntri+[[(0,0,1),(1,1,1)]]*nmatch):
  new={}
  for (j,p),v in pol.items():
   for dj,dp,mul in opts:
    key=j+dj,p+dp;new[key]=new.get(key,0)+v*mul
  pol=new
 ans=Fraction(ntri)
 for (j,p),v in pol.items():
  for k in range(max(1,p),min(a-j,b)+1):
   if k==1 and j==0:continue
   if a-j-p<k-p:continue
   ans+=Fraction(v*math.comb(a-j-p,k-p)*math.comb(b,k)*2**p*math.factorial(k)*math.factorial(k-1),2)
 assert ans.denominator==1
 return ans.numerator

def checks():
 for a,b,nt,nm in [(5,3,1,1),(6,2,2,0),(4,3,0,2)]:
  ed=[(u,a+v)for u in range(a)for v in range(b)]
  for i in range(nt):ed +=[(3*i,3*i+1),(3*i+1,3*i+2),(3*i,3*i+2)]
  for i in range(nm):ed +=[(3*nt+2*i,3*nt+2*i+1)]
  assert brute(a+b,ed)==a_components_cycles(a,b,nt,nm)
 print('General finite triangle+matching formula brute-checked.')
 for m in [10,20,40,80,160]:
  F=a_components_cycles(m,m,2,(m-6)//2)
  G=matching_both(m,m,m//2,2)
  print('n',2*m,'alternative/edgeopt',float(Fraction(G,F)),'m*(G/F-1)',float(m*(Fraction(G,F)-1)))
  if m>=20:assert G>F
if __name__=='__main__':checks()
