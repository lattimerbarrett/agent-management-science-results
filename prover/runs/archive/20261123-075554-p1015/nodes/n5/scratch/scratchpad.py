# Audit of the reductions in the padding argument.
# P is Pi^0_2, H is c.e. complete, T = H join complement(H).
# B = P join H; C = complement(B) = complement(P) join complement(H).
import networkx as nx
G = nx.DiGraph()
steps = [
 ('B', 'P', 'H is c.e., so adjoining H does not change e-degree'),
 ('P', 'B', 'projection'),
 ('C', 'T', 'complement(P) is c.e. in H, and T gives both oracle answers'),
 ('T', 'C', 'C enumerates complement(H), while H is c.e.'),
 ('complement(T)', 'T', 'swap the two columns of T'),
]
for a,b,reason in steps:
    G.add_edge(a,b)
    print(f'{a} <=_e {b}: {reason}')
print('B equivalent to P:', nx.has_path(G,'B','P') and nx.has_path(G,'P','B'))
print('C equivalent to total representative T:', nx.has_path(G,'C','T') and nx.has_path(G,'T','C'))
print('No step asserts that complement(C) <=_e C.')