from fractions import Fraction

def cubic_lower(n):
    return Fraction(n*(6*n-(27 if n%4==2 else 33)),4)

def degree_upper(n,d):
    bounds=[Fraction(n*d*(3*(n//(d+1))-1)),Fraction(n*d*max(2,n-2*d+1))]
    if d%2==0:bounds.append(Fraction(n*d*(n-1),3))
    if 2*d-n+2>0:bounds.append(Fraction(2*n*d,2*d-n+2))
    return min(bounds)

for n in [10,12,14,16,20,30,40,50,100]:
    lb=cubic_lower(n)
    contenders=[d for d in range(4,n) if degree_upper(n,d)>lb]
    print('n',n,'lower',lb,'general upper',max(degree_upper(n,d) for d in range(2,n)))
    print('higher degrees still potentially competitive:',contenders)

# Exact cap resistances, used only to verify the explicit lower constructions.
import sympy as s

def resistance(n,edges,u,v):
    L=s.zeros(n)
    for a,b in edges:
        L[a,a]+=1;L[b,b]+=1;L[a,b]-=1;L[b,a]-=1
    ids=[i for i in range(n) if i!=v]
    Q=L.extract(ids,ids)
    return Q.inv()[ids.index(u),ids.index(u)]
cap5=[(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,4)]
cap7=[(0,1),(0,5),(0,6),(1,2),(1,6),(2,3),(2,4),(3,4),(4,5),(5,6)]
print('cubic cap resistances',resistance(5,cap5,3,2),resistance(7,cap7,3,0))
