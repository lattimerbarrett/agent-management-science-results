import pickle,time,gmpy2
labs,rows,N=pickle.load(open('workspace/agent3_coupled_exact_sparse.pkl','rb'))
d=pickle.load(open('workspace/agent3_exact_dual_witness.pkl','rb'))
acc=[gmpy2.mpq(0) for _ in range(N)]
t=time.time()
for i,c in d['coefficients'].items():
 cc=gmpy2.mpq(str(c))
 for j,v in rows[i].items():acc[j]+=cc*gmpy2.mpq(v.numerator,v.denominator)
assert all(a==0 for a in acc)
P=d['prime'];vv={i:int(gmpy2.numer(gmpy2.mpq(str(c)))%P)*pow(int(gmpy2.denom(gmpy2.mpq(str(c)))%P),P-2,P)%P for i,c in d['coefficients'].items()}
assert all(int(gmpy2.denom(gmpy2.mpq(str(c)))%P) for c in d['coefficients'].values())
p,ll,m,fl=pickle.load(open('workspace/agent1_coupled_small_matrix.pkl','rb'));assert labs==ll and p==P
res=sum(vv[i]*fl[i] for i in vv)%P
assert res==448507==d['nonzero_residue']
print('INDEPENDENT GMP exactcheck: ALL1908QQidentitieszero;normalized12A+Bδ residue',res,'mod',P,'seconds',time.time()-t)
from pathlib import Path
if Path(__file__).resolve()!=Path('workspace/agent4_exact_witness_check.py').resolve():
 source=Path(__file__).read_text()
 Path('workspace/agent4_exact_witness_check.py').write_text(source)
