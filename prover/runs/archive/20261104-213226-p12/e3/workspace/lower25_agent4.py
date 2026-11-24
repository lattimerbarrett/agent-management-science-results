import itertools, math, functools, json, os
P=1000003

def parts(n,lo=1):
 if not n:yield ()
 else:
  for a in range(lo,n+1):
   for t in parts(n-a,a):yield (a,)+t

def oddfact(n):return math.prod(range(1,n+1,2))%P
invdf={i:pow(oddfact(2*i+1),-1,P) for i in range(24)}
@functools.lru_cache(None)
def blocks_poly(t):
 if not t:return (1,)
 first=t[0];rem=t[1:];distinct=sorted(set(rem));counts=[rem.count(x) for x in distinct];out=[0]*(len(t)+1)
 for sel in itertools.product(*[range(c+1) for c in counts]):
  total=first+sum(a*b for a,b in zip(distinct,sel));size=1+sum(sel)
  coeff=math.prod(math.comb(a,b) for a,b in zip(counts,sel))*invdf[total]*(-1 if size%2==0 else 1)%P
  leftover=tuple(x for x,c,k in zip(distinct,counts,sel) for _ in range(c-k))
  for k,v in enumerate(blocks_poly(leftover)):out[k+1]=(out[k+1]+coeff*v)%P
 return tuple(out)
const=oddfact(49)*pow(math.factorial(49)%P,-1,P)%P
facts=[math.factorial(47+k)%P for k in range(24)]
def integral(t):return const*sum(v*facts[k] for k,v in enumerate(blocks_poly(t)))%P
rows=list(parts(12));cols=list(parts(11));M=[[integral(tuple(sorted(a+b))) for b in cols] for a in rows]
N=[row[:] for row in M];piv=[];pivot_rows=[];order=list(range(77));rank=0
for j in range(56):
 i=next((i for i in range(rank,77) if N[i][j]),None)
 if i is None:continue
 N[rank],N[i]=N[i],N[rank];order[rank],order[i]=order[i],order[rank];pivot_rows.append(order[rank])
 inv=pow(N[rank][j],-1,P);N[rank]=[v*inv%P for v in N[rank]]
 for i in range(rank+1,77):
  c=N[i][j]
  if c:N[i]=[(a-c*b)%P for a,b in zip(N[i],N[rank])]
 piv.append(j);rank+=1

def determinant_mod(mat):
 a=[r[:] for r in mat];det=1
 for j in range(len(a)):
  i=next(i for i in range(j,len(a)) if a[i][j])
  if i!=j:a[i],a[j]=a[j],a[i];det=-det
  det=det*a[j][j]%P;inv=pow(a[j][j],-1,P)
  for i in range(j+1,len(a)):
   f=a[i][j]*inv%P
   for k in range(j+1,len(a)):a[i][k]=(a[i][k]-f*a[j][k])%P
 return det
minor_det=determinant_mod([[M[i][j] for j in piv] for i in pivot_rows])
assert rank==43 and minor_det==60513
print('pairing dimensions',len(rows),len(cols),'rank',rank,'minor determinant',minor_det)
print('minor row indices',pivot_rows,'minor col indices',piv)
os.makedirs('workspace',exist_ok=True)
json.dump({'prime':P,'rows':rows,'cols':cols,'matrix':M,'rank':rank,'pivcols':piv,'pivrows':pivot_rows,'minor_det':minor_det},open('workspace/pairing25_agent4.json','w'))
