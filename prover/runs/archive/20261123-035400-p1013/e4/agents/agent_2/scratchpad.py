import json

def turan(n,r):
 q,s=divmod(n,r)
 return (n*n-(r-s)*q*q-s*(q+1)*(q+1))//2

def check_quad():
 out={}
 for r in range(2,31):
  best=(-1,None)
  for n in range(1,301):
   for m in range((n+r-1)//r,n+1):
    # Other r-1 parts balanced maximize edges for fixed largest part m.
    e=m*(n-m)+turan(n-m,r-1)
    # doubled excess, no floating point
    numerator=r*(2*e+m-2*turan(n,r))-n
    # Continuous bound: excess <= (r-1)/(8r)+r/8.
    assert 4*numerator <= r*r+r-1
    if numerator>best[0]: best=(numerator,(n,m))
  out[r]={'max_excess_numerator_over_2r':best[0],'n_m':best[1]}
 return out

out=check_quad()
with open('workspace/gap_quadratic_agent2.json','w') as f: json.dump(out,f,indent=2)
with open('workspace/gap_quadratic_agent2.py','w') as f: f.write(open(__file__).read())
print('Exact integer quadratic optimization checked for 2<=r<=30,1<=n<=300; results saved.')
print(out)
