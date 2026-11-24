import json,pickle
from sage.all import matrix,QQ
cols,rels,labels=pickle.load(open('workspace/agent3_fz_QQ.pkl','rb'))
idx={p:i for i,p in enumerate(cols)}
D=json.load(open('workspace/agent3_radical.json'))
rad=[QQ(0)]*len(cols)
for m,c in zip(D['monomials'],D['coefficients']):rad[idx[tuple(m)]]=QQ(c)
odd=[p for p in cols if all(x%2 for x in p)]
H=[[int(j==idx[p]) for j in range(len(cols))] for p in odd]
print('Exact FZ rank',matrix(QQ,rels).rank())
print('Odd-kappa Hodge monomials',len(odd))
print('Exact FZ+Hodge rank',matrix(QQ,rels+H).rank())
print('Exact FZ+Hodge+radical rank',matrix(QQ,rels+H+[rad]).rank())
