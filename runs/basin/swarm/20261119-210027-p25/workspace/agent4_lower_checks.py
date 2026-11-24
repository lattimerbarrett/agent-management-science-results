import networkx as nx, itertools, json, os

def subdivision3(F):
    G=nx.Graph(); G.add_nodes_from(('v',v) for v in F)
    for j,(u,v) in enumerate(F.edges()):
        G.add_edges_from([(('v',u),('a',j)),(('a',j),('b',j)),(('b',j),('v',v))])
    return G

def odd_walk_graph(G):
    W=nx.Graph(); W.add_nodes_from(G)
    for u in G:
        reach=set(G[u])
        for a in G[u]:
            for b in G[a]: reach.update(G[b])
        if u in reach: raise ValueError('triangle/odd short closed walk')
        W.add_edges_from((u,v) for v in reach)
    return W

def has_cycle(G,k):
    def search(path):
        if len(path)==k:return G.has_edge(path[-1],path[0])
        return any(search(path+[v]) for v in G[path[-1]] if v not in path)
    return any(search([s]) for s in G)

def profile_target(G,col):
    typ={u:(col[u],frozenset(col[v] for v in G[u])) for u in G}
    H=nx.Graph(); H.add_nodes_from(typ.values())
    H.add_edges_from((typ[u],typ[v]) for u,v in G.edges())
    assert nx.number_of_selfloops(H)==0
    return H,typ

results=[]
for t in range(2,9):
    F=nx.complete_graph(t); G=subdivision3(F); W=odd_walk_graph(G)
    assert not has_cycle(G,3) and not has_cycle(G,5)
    assert all(W.has_edge(('v',u),('v',v)) for u,v in F.edges())
    color=nx.coloring.greedy_color(W,strategy='largest_first')
    H,typ=profile_target(G,color)
    assert not has_cycle(H,3)
    assert all(H.has_edge(typ[u],typ[v]) for u,v in G.edges())
    results.append({'base_K':t,'vertices':len(G),'edges':G.number_of_edges(),'W3_colors_used':len(set(color.values())),'profile_target_vertices':len(H)})
print(json.dumps(results,indent=2))
# Exact finite cyclic-lift construction: KG(7,3), supports t=3.
import numpy as np
m,k,t=7,3,3
s=m-2*k
sets=list(map(frozenset,itertools.combinations(range(m),k)))
F=nx.Graph(); F.add_nodes_from(range(len(sets)))
F.add_edges_from((a,b) for a in F for b in F if a<b and sets[a].isdisjoint(sets[b]))
universe=list(map(frozenset,itertools.combinations(range(m),t)))
S={a:{j for j,C in enumerate(universe) if 2*len(sets[a]&C)>t+s} for a in F}
W=odd_walk_graph(F)
assert all(S[a].isdisjoint(S[b]) for a,b in W.edges())
G=nx.Graph()
for layer in range(3):
    for j in range(len(universe)):
        G.add_edge(('U',layer,j),('X',layer))
    for a in F:
        G.add_node(('v',layer,a))
        G.add_edges_from((('v',layer,a),('U',layer,j)) for j in S[a])
for a,b in F.edges():
    for layer in range(3):G.add_edge(('v',layer,a),('v',(layer+1)%3,b))
A=nx.to_numpy_array(G,dtype=np.int64)
A2=A@A
assert np.trace(A2@A)==0
assert np.trace(A2@A2@A)==0
# Equal image tuples on any F-edge force all three cyclic pair edges.
for a,b in F.edges():
    assert all(G.has_edge(('v',i,a),('v',(i+1)%3,b)) for i in range(3))
lift_result={'m':m,'k':k,'t':t,'base_vertices':len(F),'base_edges':F.number_of_edges(),'universe_size':len(universe),'support_sizes':sorted(set(map(len,S.values()))),'lift_vertices':len(G),'lift_edges':G.number_of_edges(),'minimum_degree':min(dict(G.degree()).values()),'trace_A3':int(np.trace(A2@A)),'trace_A5':int(np.trace(A2@A2@A))}
print('LIFT',json.dumps(lift_result))
with open('workspace/agent4_lift_checks.json','w') as f: json.dump(lift_result,f,indent=2)
# Hypergeometric support ratios, computed by exact integer counts.
from math import comb
ratios=[]
for m,k,t in [(2001,999,101),(20001,9999,401),(200001,99999,4001)]:
    s=m-2*k
    numerator=sum(comb(k,j)*comb(m-k,t-j) for j in range((t+s)//2+1,min(t,k)+1))
    denominator=comb(m,t)
    p=numerator/denominator
    ratios.append({'m':m,'k':k,'s':s,'t':t,'support_fraction':p,'limiting_min_degree_ratio':p/(3*(1+p))})
print('SUPPORT RATIOS',json.dumps(ratios))
with open('workspace/agent4_support_ratios.json','w') as f: json.dump(ratios,f,indent=2)
# Shift-graph elementary replacement, checked without enumerating permutations.
k,m=7,11
tuples=list(itertools.combinations(range(m),k)); index={a:i for i,a in enumerate(tuples)}
F=nx.Graph(); F.add_nodes_from(range(len(tuples)))
for i,a in enumerate(tuples):
    F.add_edges_from((i,index[a[1:]+(b,)]) for b in range(a[-1]+1,m))
W=odd_walk_graph(F)
coeff=[]
for a in tuples:
    v=np.zeros(m,dtype=np.int64)
    for j,b in enumerate(a):v[b]=(-1)**j
    coeff.append(v)
assert all(sum(abs(coeff[u]+coeff[v]))<=6 for u,v in W.edges())
# For safe-minimum supports, any safe even-position elements lie in both tuples,
# and cannot be the same ground element on an odd walk of length at most three.
safe_positions=[j for j in range(1,k+1) if j%2==0 and 4<=j<=k-3]
for u,v in W.edges():
    A,B=tuples[u],tuples[v]
    EU={A[j-1] for j in safe_positions}; EV={B[j-1] for j in safe_positions}
    assert EU.issubset(B) and EV.issubset(A) and EU.isdisjoint(EV)
A=nx.to_numpy_array(F,dtype=np.int64); A2=A@A
assert np.trace(A2@A)==np.trace(A2@A2@A)==0
shift={'k':k,'m':m,'vertices':len(F),'edges':F.number_of_edges(),'W3_edges':W.number_of_edges(),'safe_even_positions':safe_positions,'support_fraction':len(safe_positions)/k,'trace_A3':int(np.trace(A2@A)),'trace_A5':int(np.trace(A2@A2@A))}
print('SHIFT',json.dumps(shift))
with open('workspace/agent4_shift_checks.json','w') as f:json.dump(shift,f,indent=2)
with open('workspace/agent4_lower_checks.py','w') as f:f.write(open('scratchpad.py').read())
os.makedirs('workspace',exist_ok=True)
with open('workspace/agent4_subdivision_checks.json','w') as f:json.dump(results,f,indent=2)
# Export reusable functions, without test driver.
source=open('scratchpad.py').read().split('results=[]')[0]
with open('workspace/agent4_graph_checks.py','w') as f:f.write(source)
