from pathlib import Path
p=Path('workspace/agent3_all_finite_checks.py')
code=p.read_text()
needle="    print('Klein projective-frame representation: gl4 -> cso6 is an isomorphism (dim16)',flush=True)"
repl=r'''    sympairs=[(0,0),(0,1),(1,1)]
    Qc=s.Matrix([[0,0,-2],[0,1,0],[-2,0,0]])
    symreps=[]
    for i in range(2):
        for j in range(2):
            A=s.zeros(2);A[i,j]=1;R=s.zeros(3)
            for col,(a,b) in enumerate(sympairs):
                for u in range(2):
                    R[sympairs.index(tuple(sorted((u,b)))),col]+=A[u,a]
                    R[sympairs.index(tuple(sorted((a,u)))),col]+=A[u,b]
            assert R.T*Qc+Qc*R==2*s.trace(A)*Qc
            symreps.append(R.reshape(9,1))
    assert s.Matrix.hstack(*symreps).rank()==4
    print('Frame representations checked: gl4 -> cso6 (dim16), gl2 -> cso3 (dim4)',flush=True)'''
assert needle in code
p.write_text(code.replace(needle,repl))
# Run only the newly added representation check, avoiding another full case run.
ns={'__name__':'verification_import'}
exec(compile(p.read_text(),str(p),'exec'),ns)
ns['verify_projective_frame_representations']()