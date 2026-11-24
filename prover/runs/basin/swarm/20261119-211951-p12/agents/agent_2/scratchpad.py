from pathlib import Path
s=Path('workspace/agent2_framed_coproduct25.py').read_text().split("a=json.load")[0]
exec(s)
import sympy as sp
from collections import Counter
from math import factorial
for h,d in [(20,10),(22,11),(24,12)]:
 A,K=rel(h,d);vals={}
 for j in range(1,d+1):
  z=(-1)**(j-1)*sp.bernoulli(j+1)/j/(j+1);vals[j]=int(z.p)*pow(int(z.q),prime-2,prime)%prime
 row=[]
 for ks in A:
  v=1
  for j,n in Counter(ks).items():v=v*pow(vals[j],n,prime)*pow(factorial(n),prime-2,prime)%prime
  row.append(v)
 print('h,d',h,d,'lambda_d quotient',list(K*vector(F,row)))