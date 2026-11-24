import pickle,json,sys
from sage.all import QQ,matrix,vector
W=pickle.load(open('workspace/agent3_exact_dual_witness.pkl','rb'))
P=W['prime'];coeff=W['coefficients'];q=W['q']
P0,labs,sol,ri,ci=pickle.load(open('workspace/agent1_coupled_small_solution.pkl','rb'));assert P0==P
invq=pow(sol[q],P-2,P)
for i,c in coeff.items():
 assert int(c.denominator())%P
 assert int(c.numerator())*pow(int(c.denominator()),P-2,P)%P==sol[i]*invq%P
print('Exactwitness reduces to known independentlyverified modularwitness scale',invq)
# Re-evaluate exact coefficient residues through independent Bell functional code.
s=open('workspace/agent3_dual_check.py').read().replace('P=1000000007',f'P={P}')
ns={'__name__':'independent_dual'};exec(s,ns)
beta=[];rho=[];betaj=[];rhoj=[]
for i,c in coeff.items():
 lab=labs[i];cm=int(c.numerator())*pow(int(c.denominator()),P-2,P)%P
 if lab[0]=='beta':
  p,a,b=lab[1];beta.append((p,a,b,cm));betaj.append((p,a,b,str(c)))
 elif lab[0]=='gamma':
  p,a=lab[1];rho.append((p,a,cm));rhoj.append((p,a,str(c)))
# Independently regenerate the59targetFZrelationsatnewprime.
code=open('workspace/agent2_fz.py').read().split('base={}; pivots=[]')[0].replace('P=1000000007',f'P={P}')
T={};exec(code,T)
A,B=ns['dual_values'](beta,rho,T['cols']);F=[(12*a+b)%P for a,b in zip(A,B)]
assert not any(sum(c*v for c,v in zip(row,F))%P for row in T['rows'])
from fractions import Fraction
D=json.load(open('workspace/agent3_radical.json'));idx={p:i for i,p in enumerate(T['cols'])};val=0
for m,c in zip(D['monomials'],D['coefficients']):
 c=Fraction(c);val+=c.numerator*pow(c.denominator,P-2,P)*F[idx[tuple(m)]]
assert val%P==W['nonzero_residue']
print('ExactliftfunctionalannihilatesALL59targetFZrelationsandδvalue=',val%P)
json.dump({'beta':betaj,'rho':rhoj,'prime':P,'delta_value':val%P},open('workspace/agent3_exact_beta_rho.json','w'))
src=open(__file__).read();open('workspace/agent3_exact_dual_functional_check.py','w').write(src)
