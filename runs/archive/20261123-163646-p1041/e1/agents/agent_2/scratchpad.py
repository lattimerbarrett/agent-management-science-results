import json,time,pickle
from sage.all import GF,matrix,LinearCode
A=json.load(open('workspace/a1_threebit_fiber3cycle_new_orbits.json'));B=json.load(open('workspace/agent2_threebit_vs_fullswitch_matches.json'))
for rec in B:
 i=rec['target'];F=int(A[i]['truth_hex'],16);G=int(rec['truth_hex'],16);S=[x for x in range(16384) if F>>x&1];T=[x for x in range(16384) if G>>x&1]
 def C(U):return LinearCode(matrix(GF(2),[[1]*len(U)]+[[x>>j&1 for x in U] for j in range(14)]).row_space().basis_matrix())
 c=C(S);d=C(T);start=time.time();r=c.is_permutation_equivalent(d,algorithm='verbose');print('TARGET',i,'dimension',c.dimension(),'EQUIVALENT',isinstance(r,tuple) and r[0],'seconds',time.time()-start,flush=True)
 assert isinstance(r,tuple) and r[0]
 pickle.dump(r[1],open('workspace/agent2_threebit_target%d_equiv_perm.pkl'%i,'wb'))
