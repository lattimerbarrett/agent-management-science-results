from math import comb,prod
from itertools import product
for bs in ([4,4,3],[5,4,4],[5,5,5],[6,6,5],[7,6,6]):
 m=sum(bs)//2;vals=[]
 for g in range(3):
  vals.append(sum(prod(comb(b-(i==g),k-(i==g))for i,(b,k)in enumerate(zip(bs,ks)))for ks in product(*[range(1,b)for b in bs])if sum(ks)==m))
 print(bs,vals)
