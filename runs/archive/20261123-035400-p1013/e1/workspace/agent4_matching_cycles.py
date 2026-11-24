import math

def polymul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c

def tricyc(s,t,edge=False):
 p=[1]
 for i in range(s//3): p=polymul(p,[1,15,9,1])
 for i in range(s%3): p=polymul(p,[1,1])
 q=[math.comb(t,j) for j in range(t+1)]
 if edge:
  q=polymul([math.comb(t-2,j) for j in range(t-1)],[1,4,1])
 twice=sum(p[b]*q[b]*math.factorial(b)*math.factorial(b-1) for b in range(1,min(s,t)+1))-s*t
 assert twice%2==0
 return twice//2+s//3

for edge in [False,True]:
 for n in [60,120,240,360]:
  vals=[(tricyc(s,n-s,edge),s,s*(n-s)+s-s%3+(1 if edge else 0)) for s in range(n//2-5,n//2+7)]
  best=max(vals)
  em=max(x[2] for x in vals)
  print('TRI',edge,n,'best s,e',best[1:],'edge-best',[(s,e) for c,s,e in vals if e==em])

def cyc(s,t,k):
    z=0
    for q in range(k+1):
      for y in range(max(q,1),min(t,s-q)+1):
        if 2*y+q<3:continue
        z+=math.comb(k,q)*2**q*math.comb(s-2*q,y-q)*math.comb(t,y)*math.factorial(y)*math.factorial(y-1)//2
    return z
