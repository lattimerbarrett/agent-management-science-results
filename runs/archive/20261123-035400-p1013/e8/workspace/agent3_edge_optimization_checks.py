from fractions import Fraction
import json
results=[]
for r in range(3,31):
 k=6 if r==3 else 8 if r==4 else 2*r+1
 rho=Fraction(k-1,k);M=12*k
 small=[0]*(M+1)
 for m in range(1,M+1):small[m]=max(small[m-j]+j-1 for j in range(1,min(k,m)+1))
 E=[]
 for m in range(M+1):
  val=small[m]
  for b in range(k+1,min(k+3,m)+1):val=max(val,b-1+small[m-b])
  E.append(val)
  if m>=k+3:assert val==3+(rho*(m-3)).numerator//(rho*(m-3)).denominator
  assert val==m-(m+k-1)//k or val>m-(m+k-1)//k
 for q in range(1,8):
  u=k*q;n=r*u+2*r+2
  # active part cannot exceed stored DP domain if M=12k and q<=7;
  # enumerate all possibilities anyway by computing E formula on demand.
  def edgeF(m):
   val=m-(m+k-1)//k
   for b in range(k+1,min(k+3,m)+1):val=max(val,b-1+(m-b)-(m-b+k-1)//k)
   return val
  vals=[]
  for m in range(n+1):
   a,t=divmod(n-m,r-1);parts=[m]+[a+1]*t+[a]*(r-1-t)
   cross=(n*n-sum(x*x for x in parts))//2
   vals.append(cross+edgeF(m))
  best=max(vals);arg=[m for m,v in enumerate(vals) if v==best]
  assert arg==[u+3],(r,k,q,arg)
  assert edgeF(u+3)==q*(k-1)+3
 results.append({'r':r,'k':k,'rho_over_r':str(rho/r),'DP_checks':M+1,'residue_checks':7})
print('passed',len(results),'r values;',sum(x['DP_checks'] for x in results),'DP identities and',sum(x['residue_checks'] for x in results),'GLOBAL residue optimizations')
with open('workspace/agent3_edge_optimization_checks.json','w') as f:json.dump(results,f)
