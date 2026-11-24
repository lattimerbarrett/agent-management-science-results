import itertools
# Quotients of three ample line bundles on F0 by one line, seeking target Chern.
L=list(itertools.product(range(1,9),repeat=2))
sol=[]
for I in itertools.combinations_with_replacement(L,3):
 A=sum(a for a,b in I);B=sum(b for a,b in I);ka=A-4;kb=B-4
 c2=sum(a*d+b*c for (a,b),(c,d) in itertools.combinations(I,2))-(A*kb+B*ka)+2*ka*kb
 if c2!=26:continue
 usable=[(a-ka,b-kb) for a,b in I if a>=ka and b>=kb]
 if len(usable)>=2:sol.append((I,(ka,kb),usable))
print('Candidates',len(sol));print(sol[:40])