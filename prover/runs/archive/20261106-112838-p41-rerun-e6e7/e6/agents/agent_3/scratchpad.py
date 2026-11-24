from pathlib import Path
s=Path('workspace/agent3_h1zero_search.py').read_text()
s=s.replace('s=z3.Solver();s.set(timeout=timeout)','s=z3.SolverFor("QF_FD");s.set(timeout=timeout)')
s=s.replace('s.add(z3.Sum([z3.If(q,1,0) for q in facebool])!=3)','\n        for j in range(4):s.add(z3.Implies(z3.And([facebool[k] for k in range(4) if k!=j]),facebool[j]))')
s=s.replace('nt=z3.Sum([z3.If(q,1,0) for q in Ts]);nf=z3.Sum([z3.If(q,1,0) for q in Fs])\n    s.add(nt>=(n-2)**2,nf>=nt-(n*(n-1)//2-n+1),nf<len(facets))','s.add(z3.PbGe([(t,1) for t in Ts],(n-2)**2))\n    s.add(z3.PbGe([(f,1) for f in Fs]+[(t,-1) for t in Ts],-(n*(n-1)//2-n+1)))\n    s.add(z3.Or([z3.Not(f) for f in Fs]))')
s=s.replace('solve(9,timeout=180000)','solve(9,timeout=1200000)')
Path('workspace/agent3_h1zero_fd_search.py').write_text(s)
exec(compile(s,'workspace/agent3_h1zero_fd_search.py','exec'))