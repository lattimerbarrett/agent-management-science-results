import sympy as s,networkx as nx,json
r,k=s.symbols('r k',integer=True,positive=True)
q=(r-1)/r;rho=(k-1)/k;L=r/((r-1)*(r-2));B=2*r/(r-1)**2;D=(k-2)*(k-3)/(2*k)
A=-2/q+2*L*(2*rho-1)+B*D
P=(r-2)*k**2+(-2*r**2+3*r+4)*k+2*r-8
factor=r/(k*(r-2)*(r-1)**2)
assert s.cancel(A-factor*P)==0
assert s.expand(P.subs(k,2*r)+2*(r-4)*(r-1))==0
assert s.expand(P.subs(k,2*r+1)-6*(r-1))==0
assert s.expand(P.subs(k,2)+4*(r-2)*(r-1))==0
assert s.expand(P.subs(r,3)-(k*k-5*k-2))==0
assert s.expand(P.subs(r,4)-2*k*(k-8))==0
count=0
for n in range(2,13):
    vals=[]
    for T in nx.nonisomorphic_trees(n):
        w=sum(d*(d-1)//2 for v,d in T.degree());vals.append(w);count+=1
        assert n-2<=w<=(n-1)*(n-2)//2
    assert min(vals)==n-2 and max(vals)==(n-1)*(n-2)//2
    assert s.Rational(max(vals)-min(vals),n)==D.subs(k,n)
# Check phase-sign cutoff directly across a wide range, not as substitute for identities above.
for R in range(3,301):
    cutoff=6 if R==3 else 8 if R==4 else 2*R+1
    for K in range(2,cutoff):assert (R-2)*K*K+(-2*R*R+3*R+4)*K+2*R-8<0
    K=cutoff
    assert (R-2)*K*K+(-2*R*R+3*R+4)*K+2*R-8>=0
result={'symbolic_A_over_P':str(factor),'unlabelled_trees_checked':count,'tree_orders':'2..12','exact_sign_ranges_checked':'r=3..300, k below first nonnegative cutoff'}
print(json.dumps(result,indent=2));open('workspace/agent2_lower_arithmetic_fast_checks.json','w').write(json.dumps(result,indent=2))
