import sys,math,json
sys.path.insert(0,'workspace')
from cycle_count_agent3 import convolve
MP=[[1]]; IP=[[1]]
for i in range(405):
 MP.append(convolve(MP[-1],[1,4,1]));IP.append(convolve(IP[-1],[1,1]))
fac=[math.factorial(i) for i in range(406)]
def poly(a,kind):
 if kind=='match':return convolve(MP[a//2],IP[a%2])
 if kind=='tri':return convolve([1,15,9,1],convolve(MP[(a-3)//2],IP[(a-3)%2]))
 if kind=='edge':return convolve([1,4,1],IP[a-2])
 if kind=='indep':return IP[a]
def cycles(a,b,kind):
 p=poly(a,'tri' if kind=='A' else 'match');q=poly(b,'indep' if kind=='A' else 'edge')
 ans=sum(p[k]*q[k]*fac[k]*fac[k-1] for k in range(1,min(a,b)+1))-a*b
 assert ans%2==0
 return ans//2+(kind=='A')
results=[]
for n in range(12,401):
 vals=[]
 for kind in ['A','B']:
  for a in range(max(3,n//2-3),n//2+5):
   e=a*(n-a)+((a-3)//2+3 if kind=='A' else a//2+1)
   vals.append((e,cycles(a,n-a,kind),kind,a))
 me=max(v[0] for v in vals);mc=max(v[1] for v in vals)
 ae={(v[2],v[3]) for v in vals if v[0]==me};ac={(v[2],v[3]) for v in vals if v[1]==mc}
 assert ae&ac,(n,ae,ac)
 results.append({'n':n,'edge_opt':sorted(ae),'cycle_opt':sorted(ac)})
json.dump(results,open('workspace/agent3_candidate_AB_results.json','w'))
print('Verified common optimum of candidate A/B within |a-n/2|<=4 for every 12<=n<=400')
