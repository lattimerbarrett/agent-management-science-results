from math import comb,log2
for n in range(5,13):
 lengths=[(n-2*j+1, comb(n,j)-(comb(n,j-1) if j else 0)) for j in range(n//2+1)]
 logbound=sum(count*log2(length+1) for length,count in lengths)
 print(n,logbound)
