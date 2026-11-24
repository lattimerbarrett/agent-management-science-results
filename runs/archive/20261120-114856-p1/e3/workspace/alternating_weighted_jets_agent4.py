from pathlib import Path
src=Path('workspace/nonsym_weighted_jets_agent4.py').read_text()
start=src.index('d=K(R(');end=src.index('\ndef mp',start)
src=src[:start]+"u=K(-1);v=K(1);bb=bd=K(R(-3,4));H=K(R(135,256));xis=[K(R(-3,4)),K(R(3,4))]\nS=u+v;T=u*v+bb+bd;L=u*bd+v*bb;C0=bb*bd-H\n"+src[end:]
src=src.replace('+H*M[-4]-2*H*sum','-C0*M[-4]-2*H*sum')
start=src.index('e=J(');end=src.index("print('done'",start)
src=src[:start]+"e=J([zero,one,zero,zero]);a=mp([J(m),p*e,-e/2,q1*e**2,q2*e**2],u,bb,v,bd);b=mp(a,v,bd,u,bb)\ncoef=[[x.as_expr() for x in row.a] for row in b]\npickle.dump(coef,open('workspace/alternating_weighted_jets_agent4.pkl','wb'))\nA=b[0].a[1];B=b[1].a[2];C=b[2].a[2];g=2*C\nF=[A,B+p*g,b[3].a[3]+2*q1*g,b[4].a[3]+2*q2*g]\npickle.dump(([x.as_expr() for x in F],g.as_expr()),open('workspace/alternating_ode_agent4.pkl','wb'))\n"+src[end:]
src=src.replace('nonsym_weighted_jets_agent4.py','alternating_weighted_jets_agent4.py')
exec(compile(src,'alternating','exec'))
