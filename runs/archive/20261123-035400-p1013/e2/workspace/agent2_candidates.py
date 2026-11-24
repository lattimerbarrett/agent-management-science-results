import sys
sys.path.insert(0,'workspace')
from agent2_candidates import min_active
import networkx as nx
for r in range(3,7):
 G=nx.path_graph(5)
 for J in [nx.cycle_graph(4)]+[nx.empty_graph(2) for _ in range(r-3)]:G=nx.convert_node_labels_to_integers(nx.full_join(G,J,rename=('a','b')))
 print('new',r,min_active(G,r))
