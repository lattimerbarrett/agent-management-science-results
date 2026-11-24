from fractions import Fraction as F
from itertools import combinations

def det(M):
 M=[r[:] for r in M];n=len(M);ans=F(1)
 for i in range(n):
  if M[i][i]==0:
   p=next((j for j in range(i+1,n) if M[j][i]),None)
   if p is None:return F(0)
   M[i],M[p]=M[p],M[i];ans=-ans
  pivot=M[i][i];ans*=pivot
  for j in range(i+1,n):
   t=M[j][i]/pivot
   for k in range(i+1,n): M[j][k]-=t*M[i][k]
 return ans

def cont(u,v,i,t):
 km2,km1=F(0),F(1)
 for k in range(i,t+1):
  new=(u[k]+v[k])*km1-(u[k-1]*v[k-1]*km2 if k>i else 0)
  km2,km1=km1,new
 return km1
checks=0
for n in range(1,11):
 u=[F((i+1)**2,17) for i in range(n)]
 v=[F((i+3)**2,23) for i in range(n)]
 Q=[[F(0)]*(n+2) for _ in range(n)]
 for i in range(n):Q[i][i:i+3]=[F(1),-u[i]-v[i],u[i]*v[i]]
 for i,j in combinations(range(n+2),2):
  w=cont(u,v,i,j-2)
  for k in range(j-1,n):w*=u[k]*v[k]
  cols=[k for k in range(n+2) if k not in [i,j]]
  assert w>0 and w==(-1)**(i+j+1)*det([[r[k] for k in cols]for r in Q]);checks+=1
for length in range(1,101):
 t=F(1,3);u=[t]*length;v=u[:]
 assert cont(u,v,0,length-1)==(length+1)*t**length
print('Exact recurrence/minor identities checked:',checks)
print('Confluent growth K_l=(l+1)t^l checked for l=1,...,100')
print('Normalized local contraction in confluent recurrence: (l/(l+1))^2, tending to 1, not a uniform constant <1.')
