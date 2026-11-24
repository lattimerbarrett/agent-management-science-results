import gmpy2 as g,numpy as np,pickle,os
from pathlib import Path
g.get_context().precision=384;M=lambda x:g.mpfr(str(x));H=M('.001');two=M(2);B=M('2.5');C=M('.5625');rc=g.sqrt(B*B-4*(C-H));re=g.sqrt(B*B-4*(C+H));oc=g.sqrt((B+rc)/2);ic=g.sqrt((B-rc)/2);ie=g.sqrt((B-re)/2)
lam=[-oc,-ic,ic,oc,-ie,ie];F=np.load('workspace/alternateH_0.001_agent3.npz');ww=F['start'][24];w=[M(ww[j])for j in[0,1,2,3,5,6]];ss=sum(w);w=[x/ss for x in w]
init='workspace/mpfr_mirror_init_agent2.pkl'
pickle.dump(dict(w=w,lam=lam,pars=(M(0),M(0),H),k=0,visits=[],side=0,hist=[],lineinterval=(-1-ic,-1+ic)),open(init,'wb'))
code=Path('workspace/mpfr_skip_agent2.py').read_text()
code=code.replace("old='workspace/mpfr384_orbit_agent2.pkl';save='workspace/mpfr_skip_agent2.pkl'","old='workspace/mpfr_mirror_init_agent2.pkl';save='workspace/mpfr_mirror_skip_agent2.pkl'")
code=code.replace('ml=one-lam[2];mr=one-lam[1]','ml,mr=D[\'lineinterval\']')
code=code.replace("Path('workspace/mpfr_skip_agent2.py')","Path('workspace/mpfr_mirror_skip_agent2.py')")
exec(compile(code,'mirror_skip','exec'))
