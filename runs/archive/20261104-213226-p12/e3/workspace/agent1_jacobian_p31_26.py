from collections import Counter,defaultdict
import math,time,json
P=1000000007;G=25;PSI=(0,-2)
def prod(mon,vs):
 coeff=1;out=list(mon)
 for i,j in vs:
  if (i,j)==PSI:out.append((i,j));continue
  if i<0 or j<0 or i>j+2 or (i+j)%2:return None,0
  if i==j==0:coeff=coeff*G%P
  else:out.append((i,j))
 return tuple(sorted(out)),coeff

def deriv(poly):
 out=defaultdict(int)
 for mon,coef in poly.items():
  c=Counter(mon); keys=[v for v in c if v[0]>0]
  for a,(i,j) in enumerate(keys):
   n=c[i,j];rest=list(mon);rest.remove((i,j))
   dest,w=prod(rest,[(i-2,j)])
   if w:out[dest]=(out[dest]+coef*n*w)%P
   for k,l in keys[a:]:
    m=c[k,l]-(i==k and j==l)
    if m<=0:continue
    factor=n*m*(pow(2,-1,P) if (i,j)==(k,l) else 1)%P
    rest2=rest[:];rest2.remove((k,l))
    dest,w=prod(rest2,[PSI,(i-1,j-1),(k-1,l-1)])
    if w:out[dest]=(out[dest]+coef*factor*w)%P
    dest,w=prod(rest2,[(i+k-2,j+l)])
    if w:out[dest]=(out[dest]-coef*factor*math.comb(i+k-2,i-1)*w)%P
 return {k:v for k,v in out.items() if v}
initial=[(3,1)]*26
poly={tuple(sorted(initial)):1}
t=time.time()
for r in range(39):
 poly=deriv(poly)
 print(r+1,len(poly),round(time.time()-t,2),flush=True)
json.dump([[k,v] for k,v in poly.items()],open('workspace/agent1_jacobian_p31_26.json','w'))
