import mpmath as mp
mp.mp.dps=40
# Compare the limiting cycle factors for bounded-degree additions
# in one class of a nearly balanced complete bipartite graph.
def factor(s,d):
    return (1+mp.mpf(d))**(mp.mpf(s)/2)*mp.besseli(abs(s),2*mp.sqrt(1+mp.mpf(d)))
for d in [1,2,3]:
    print('d=',d,'F1=',mp.nstr(factor(1,d),18),'F3=',mp.nstr(factor(3,d),18),'ratio=',mp.nstr(factor(3,d)/factor(1,d),18))
for m in [10,100]:
    n=8*m+3
    candidates=[]
    for a in range(n+1):
        b=n-a
        candidates.append((a*b+(3*a)//2+1,a,b))
    print('n=',n,'max candidate edge count:',max(candidates))
    for a in [4*m+2,4*m+3]:
        b=n-a
        print('  sizes=',(a,b),'candidate edges=',a*b+(3*a)//2+1)
