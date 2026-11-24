import mpmath as mp
import networkx as nx
mp.mp.dps=50
# Limiting cycle factors for a cubic internal graph in one bipartition class.
for s in (1,3):
    F=mp.power(4,mp.mpf(s)/2)*mp.besseli(s,4)
    print('s =',s,'factor =',F)
print('ratio F3/F1 =',4*mp.besseli(3,4)/mp.besseli(1,4))
Q=nx.complete_graph(5)
Q.remove_edges_from([(0,1),(1,2),(3,4)])
print('Q degrees:',sorted(dict(Q.degree()).values()),'edges:',Q.number_of_edges())
# Compare the edge objectives for odd n = 8j+7.
for j in (1,2,10):
    n=8*j+7
    vals=[(A*(n-A)+(3*A)//2+1,A) for A in range(n+1)]
    mx=max(x[0] for x in vals)
    print('n',n,'maximizing part sizes',[A for e,A in vals if e==mx],
          'candidate deficit',mx-((n+3)//2*((n-3)//2)+(3*((n+3)//2))//2+1))