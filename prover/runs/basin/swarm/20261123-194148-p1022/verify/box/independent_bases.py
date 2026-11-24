import sys
sys.path.insert(0,'workspace')
import agent1_final_verification as f
import sympy as s
for n,ranks in [(2,(1,1,1)),(3,(1,3,1)),(3,(1,2,2)),(4,(1,5,1)),(4,(1,4,2)),(4,(2,3,2)),(4,(1,3,3))]:
 eq,vs,sub,G,P=f.solve_case(n,ranks)
 L=G.fglm('lex')
 print(n,ranks,vs, '\nlex:', list(L))
 # Stronger proof of completeness: each polynomial vanishing at listed points
 # has nilpotent class in original zero-dimensional coordinate ring.
 # The explicit lex basis exposes the possible roots.
 print('solutions', [tuple(p[v] for v in vs) for p in P])
