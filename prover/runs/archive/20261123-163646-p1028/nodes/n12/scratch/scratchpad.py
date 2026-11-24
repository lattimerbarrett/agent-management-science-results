import networkx as nx, numpy as np, sympy as s, pickle
R=pickle.load(open('search_results.pkl','rb'))
for n,d in [(14,5),(14,3),(15,6),(15,4),(17,4),(19,4),(21,4),(23,4),(25,4)]:
 val,A,u,v=R[n,d];G=nx.from_numpy_array(A)
 print('\n',n,d,'commute',val,'pair',u,v,'articulations',list(nx.articulation_points(G)))
 for vs in nx.biconnected_components(G):
  H=G.subgraph(vs)
  arts=[a for a in vs if a in set(nx.articulation_points(G))]
  print(' block',len(vs),'degrees',sorted(dict(H.degree()).values()),'art',arts, 'target',[a for a in [u,v] if a in vs])
  if len(vs)>2:print(' edges',list(H.edges()))

# Dense odd-degree barbell, reduced to a cubic chain on the same n.
d=s.symbols('d',positive=True)
x,y,z=s.symbols('x y z')
sol=s.solve([(d-1)*(x-z)-1,d*y-(d-1)*z,3*z-x-y], [x,y,z])
r_end=s.factor(sol[x])
print('\nOdd-degree dense end resistance:',r_end)
old_scaled=d*(1+2*r_end)
new_scaled=3*(d-s.Rational(1,4))
print('Cubic replacement commute improvement / n:',s.factor(new_scaled-old_scaled))
# Dense even-degree articulation family. An end has root degree a,
# all other d+1 vertices degree d; join ends with a=2 and a=d-2.
a=s.symbols('a',positive=True)
sol=s.solve([a*(x-z)-1,(a+1)*y-a*z,(d+2-a)*z-x-(d-a)*y], [x,y,z])
r_end_even=s.factor(sol[x])
print('Even-degree dense end resistance:',r_end_even)
old_even_scaled=s.factor(d*(r_end_even.subs(a,2)+r_end_even.subs(a,d-2)))
print('Dense even-degree commute / n:',old_even_scaled)
print('Improvement using quartic lower bound n*(n-7), divided by n:',s.factor(2*d-4-old_even_scaled))
for degree in [6,8,10,12]:
 n=2*degree+3
 low=R.get((n,4))
 print('degree',degree,'n',n,'dense commute',s.factor(n*old_even_scaled.subs(d,degree)),
       'quartic candidate',None if low is None else low[0], 'guaranteed comparison bound',n*(n-7))
