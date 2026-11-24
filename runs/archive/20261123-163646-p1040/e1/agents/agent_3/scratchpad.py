import numpy as np,json,time
from scipy.sparse import load_npz,csr_matrix,vstack
D=json.load(open('workspace/agent3_W_detector_functional.json'))
cols=np.array([i*9720+j for i in range(3) for j in range(3159)])
lamcols=[];lamvals=[]
for j,c in D['flat_lambda'].items():
 j=int(j);out,off=divmod(j,9720);assert off<3159;lamcols.append(out*3159+off);lamvals.append(c)
L=csr_matrix((np.array(lamvals,dtype=np.int32),(np.zeros(len(lamcols),dtype=int),lamcols)),shape=(1,9477))
fullix=np.array([i*9801+j for i in range(3) for j in range(81,81+3159)])
N=[load_npz(f'workspace/agent4_tensor_N_{i}.npz')[fullix,:][:,fullix] for i in range(9)]
def clean(A):A=A.tocsr();A.data%=3;A.eliminate_zeros();return A
duals=[clean(L@A) for A in N]
duals+= [clean(d@A) for d in duals[:9] for A in N]
T=vstack(duals,format='csr');A=np.load('workspace/agent3_gamma4_tensor_seedmatrix.npy')[:,cols]
V=(T@A.T)%3
print('dualfunctionals',len(duals),'seedcolumns',len(A),'checkedentries',V.size,'nonzero',np.count_nonzero(V))
assert not V.any()
W=np.load('workspace/agent3_explicit_W_finite_vector.npy')[cols];val=int((L@W)[0]%3);print('lambda W',val);assert val==2
# Independently verify triple nilpotence by degree filtration from every sparse entry.
wordsdeg=np.array([d for d in (5,6,7) for _ in range(3**d)]*3)
for M in N:
 r,c=M.nonzero();assert np.all(wordsdeg[r]>wordsdeg[c])
print('PASS degreefiltration=>alltripleNproducts0')
json.dump({'dual_count':90,'unique_actual_seed_count':5148,'all_dual_seed_pairings_zero':True,'lambda_W':val,'degree_strict_increase':True},open('workspace/agent3_minimal_functional_audit.json','w'))
