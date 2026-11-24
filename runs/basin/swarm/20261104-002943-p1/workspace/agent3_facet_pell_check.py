from pathlib import Path
exec(compile(Path('workspace/agent3_facet_Q2_generate.py').read_text(),'facetgen','exec'))
Z=x*x+(a+2)*x+(-2*a*a-4*a+10)/(a-2);zc=vector(K,[Z[j] for j in range(4)])
q2=sum((res[(i,j)]*zc[i]*zc[j] for i in range(4) for j in range(i,4)),vector(K,4));assert q2==vector(K,4)
eta=[(P*Z).mod(D),R.zero(),(-E*P*Z).mod(D)];out=fitjet(fitjet([w,eta,zero],pq),qq);dr=add(out[1],neg(eta))
assert integ(dr[0]*dr[0])==0 and integ(dr[1]*dr[1])==0
M0inv=mm(w)[0].inverse();g=(kk*Z).mod(D);co=M0inv*vector(K,[integ(P*g*x**j) for j in range(4)]);target=4*(g-integ(g)-P*sum(co[j]*x**j for j in range(4))).mod(D)
assert integ((dr[2]-target)**2)==0
print('Facet Pell normal Q2(Z)=0 EXACT; leading/first shear vanish; second shear equals Fisher gradient of fixed functional k*Z.')
