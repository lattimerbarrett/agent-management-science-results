import sys,math
from fractions import Fraction
sys.path.insert(0,'workspace')
from agent2_cycles import matching_both,brute

def onepart(a,b,matching_edges,triangles):
 assert 2*matching_edges+3*triangles<=a
 coeff={(0,0):1}
 for opts,times in [([(0,0,1),(1,1,1)],matching_edges), ([(0,0,1),(1,1,3),(2,1,3)],triangles)]:
  for _ in range(times):
   ne={}
   for (j,p),v in coeff.items():
    for dj,dp,mul in opts:
     key=j+dj,p+dp;ne[key]=ne.get(key,0)+v*mul
   coeff=ne
 ans=Fraction(triangles)
 for (j,p),v in coeff.items():
  for k in range(max(1,p),min(a-j,b)+1):
   if k==1 and j==0:continue
   if a-j-p<k-p:continue
   ans+=Fraction(v*math.comb(a-j-p,k-p)*math.comb(b,k)*2**p*math.factorial(k)*math.factorial(k-1),2)
 assert ans.denominator==1
 return ans.numerator

def run_checks():
 # Exhaustive independent cycle-count check for a small mixed component graph.
 a,b=5,3;edges=[(i,a+j) for i in range(a) for j in range(b)]+[(0,1),(1,2),(0,2),(3,4)]
 assert brute(a+b,edges)==onepart(a,b,1,1)
 for n in [24,40,80,120,200,400]:
  m=n//2
  edgeext=onepart(m,m,m//2-3,2)
  alternative=matching_both(m,m,m//2,2)
  baseline=matching_both(m,m,m//2,0)
  print(n,'alternative/edgeext',float(Fraction(alternative,edgeext)), 'm-scaled difference/base',float(Fraction(m*(alternative-edgeext),baseline)),flush=True)
  if n>=40: assert alternative>edgeext
if __name__=='__main__':run_checks()
