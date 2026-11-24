import networkx as nx
from fractions import Fraction
import json

def theta(L):
    G=nx.Graph(); G.add_nodes_from([0,1]); nxt=2
    for j in range(3):
        p=[0]+list(range(nxt,nxt+L-1))+[1]; nxt+=L-1
        G.add_edges_from(zip(p,p[1:]))
    return G

results=[]
for L in range(2,6):
    G=theta(L); E=list(G.edges()); rho=Fraction(G.number_of_edges(),G.number_of_nodes())
    maxproper=Fraction(0)
    for mask in range(1,1<<len(E)):
        F=nx.Graph(); F.add_edges_from(E[j] for j in range(len(E)) if mask>>j&1)
        dens=Fraction(F.number_of_edges(),F.number_of_nodes())
        assert dens<=rho
        if mask!=(1<<len(E))-1:
            assert dens<=1
            maxproper=max(maxproper,dens)
    rec={'L':L,'v':G.number_of_nodes(),'e':len(E),'density':str(rho),'proper_max_density':str(maxproper),'subgraphs_checked':2**len(E)-1}
    results.append(rec)
print(json.dumps(results,indent=2))
with open('workspace/agent3_theta_density.json','w') as f: json.dump(results,f,indent=2)
with open('workspace/agent3_theta_density.py','w') as f: f.write(open(__file__).read())
