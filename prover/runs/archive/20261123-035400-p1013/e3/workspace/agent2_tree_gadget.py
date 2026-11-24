import networkx as nx,json

def tree_gadget(T,s=None):
 s=len(T)-1 if s is None else s
 a=next(x for x in T if T.degree(x)==1);v=next(iter(T[a]));B=set(T[v])-{a};d=T.degree(v)
 col=nx.single_source_shortest_path_length(T,v);UX={x for x in T if x not in {a,v}|B and col[x]%2==1};UY=set(T)-{a,v}-B-UX
 G=nx.relabel_nodes(T,lambda x:('q',x));A=('q',a);V=('q',v);BB={('q',x) for x in B};XX={('q',x) for x in UX};YY={('q',x) for x in UY}
 L={('l',i) for i in range(s)};D={('d',i) for i in range(s-d)};c=('l',0)
 G.add_edges_from((A,x) for x in L);G.add_edges_from((V,x) for x in L|D);G.add_edges_from((c,x) for x in BB|XX);G.add_edges_from((u,z) for u in D for z in YY)
 return G,{'v':V,'L':L,'D':D,'A':A,'B':BB,'X':XX,'Y':YY,'c':c}

def contains(G,H):return nx.algorithms.isomorphism.GraphMatcher(G,H).subgraph_is_monomorphic()

