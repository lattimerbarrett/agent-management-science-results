"""Reproduce ALL finite certificates for integral degree-two injectivity.
Run python workspace/agent2_verify_degree2_all_ranks.py from working directory.
All group identities are verified as exact tuples of reduced free words.
No precomputed results are trusted: pickle helper files are overwritten.
"""
import sys,pickle
sys.path.insert(0,'workspace')
from agent2_source_relations import lattice_relations
from agent2_gl_closure import close_GL,bracket_matrix
from agent2_sparse_closure import UnitLattice,johnson_columns,run,certify
import sympy as S
for n in [3,4]:
    G,P,R,H=lattice_relations(n=n,depth=3)
    pickle.dump((G,P,R,H),open(f'workspace/agent2_ia{n}_quadratic_relations.pkl','wb'))
    B=close_GL(n,H)
    J=bracket_matrix(n)
    assert J*B==S.zeros(J.rows,B.cols)
    assert J.rank()+B.cols==J.cols
    pickle.dump(B,open(f'workspace/agent2_ia{n}_GL_relations.pkl','wb'))
    print('CERTIFIED SOURCE',n,'relations',B.cols,'bracket rank',J.rank(),flush=True)
for n in [2,3,4]:
    L=UnitLattice()
    for c in johnson_columns(n):L.insert(c)
    assert len(L.b)==n*n*(n*n-1)//3-n*(n+1)//2
    print('Primitive bracket image',n,'rank',len(L.b),'blocked',L.blocked,flush=True)
for n in [5,6]:certify(n,run(n))
print('ALL FINITE CERTIFICATES VERIFIED',flush=True)
