from fractions import Fraction as F
from math import comb
import json, os

def binom(a,l):
    r=F(1)
    for i in range(l):r*= (a-i)/(i+1)
    return r

def pmul(a,b):
    c={}
    for i,v in a.items():
      for j,w in b.items(): c[i+j]=c.get(i+j,0)+v*w
    return {i:v for i,v in c.items() if v}

def matrix(g,b,kind):
    r=(g+2)//3;k=g-r;N=4*g-3;c=2-2*g;M=4*g+2
    rows={}; idx=0
    for n in range(N):
      for typ in (('h','v') if kind=='S' else ('f',)):
       R=3*n+4*g+(typ=='v')
       for j in range(-R,0): rows[n,typ,j]=idx;idx+=1
    psi={k-(2*g-1-2*j):F(v) for j,v in enumerate(b) if v}
    deriv={i-1:(i-k)*v for i,v in psi.items()}
    pw=[{0:F(1)}]
    for l in range((N-1)//k+1):pw.append(pmul(pw[-1],psi))
    cols=[]
    for n in range(N):
      for typ in (('h','v') if kind=='S' else ('f',)):
       q=(kind=='L' or typ=='h')
       lim=4*n+(2*g+2 if q else 4*g+(typ=='v'))
       ds=[d for d in range(lim+1) if d%2==0 or d>=2*g+1]
       alpha=F(1)-F(n,k) if kind=='L' or typ=='v' else -F(n,k)
       for d in ds:
        col={}; eps=d%2
        for l in range((N-1-n)//k+1):
         fac=binom(alpha,l)*(-k)**l*(-F(1,2) if q else 1)
         p={j:fac*v for j,v in pw[l].items()}
         terms=[(n+l*k,typ,p,0)]
         if typ=='h':
          terms=[(n+l*k,'h',p,0),(n+l*k,'v',{j:-v for j,v in p.items()},-1)]
          if n+(l+1)*k<N:terms.append((n+(l+1)*k,'v',{j:-v for j,v in pmul(p,deriv).items()},0))
         for m,tp,poly,shift in terms:
          for j,v in poly.items():
           e=n-d+(c if q else 0)+j+shift
           for z in range(max(0,(-1-e)//M+1)):
            exponent=e+M*z
            coeff=v*binom(F(eps+q,2),z)*(-1)**z
            if coeff:
             assert (m,tp,exponent) in rows,(g,n,d,m,tp,exponent)
             ii=rows[m,tp,exponent];col[ii]=col.get(ii,0)+coeff
        cols.append({i:v for i,v in col.items() if v})
    return idx,cols

def rankmod(cols,p=1000000007):
    piv={}
    for col in cols:
      a={i:int(v.numerator)*pow(int(v.denominator),-1,p)%p for i,v in col.items()}
      a={i:v for i,v in a.items() if v}
      while a:
       i=min(a);v=a[i]
       if i not in piv:
        inv=pow(v,-1,p);piv[i]={j:w*inv%p for j,w in a.items()};break
       for j,w in piv[i].items():
        a[j]=(a.get(j,0)-v*w)%p
        if not a[j]: del a[j]
    return len(piv)

def rankexact(cols):
    piv={}
    for col in cols:
      a=dict(col)
      while a:
       i=min(a);v=a[i]
       if i not in piv:
        piv[i]={j:w/v for j,w in a.items()};break
       for j,w in piv[i].items():
        a[j]=a.get(j,0)-v*w
        if not a[j]: del a[j]
    return len(piv)

if __name__=='__main__':
 for g in range(2,8):
  r=(g+2)//3
  for b in [[0]*r]+[[int(j==i) for j in range(r)] for i in range(r)]+[[comb(r-1,j) for j in range(r)]]:
   hs=[]
   for kind in ['O','S','L']:
    rows,cols=matrix(g,b,kind)
    rank=rankexact(cols)
    assert rank==rankmod(cols)
    hs.append(rows-rank)
   delta=hs[0]-hs[1]+hs[2]
   s=1+max([j for j,v in enumerate(b) if v],default=-1)
   expected=1-s
   assert delta==expected,(g,b,hs,delta,expected)
   if s:
    total=s*(g+r+1-2*s)
    assert hs[0]==g*g+1-total
    assert hs[2]==5*g*g-7*g+3-total
    assert hs[1]==6*g*g-7*g+3-2*total+s
   else:
    assert hs==[g*g,6*g*g-7*g+2,5*g*g-7*g+3]
   print(g,b,hs,delta,flush=True)
 os.makedirs('workspace',exist_ok=True)
 with open('workspace/agent4_laurent_matrix.py','w') as f:
  f.write(open('scratchpad.py').read())
