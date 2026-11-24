from pathlib import Path
p=Path('workspace/agent4_spectral_identity_checks.py');t=p.read_text()
extra='''\n# Exact transfer from target-normalized Euclidean action to unit hemisphere.\nA=4*(n-1)/(n-2); cn=(n-2)/(4*(n-1))\nassert s.simplify(A*cn-1)==0\nassert s.simplify(A*n*(n-2)-4*n*(n-1))==0\nassert s.simplify(2/(A*A*2**(n-2))-2**(3-n)/A**2)==0\nassert s.simplify((2**(3-n)/A**2).subs(n,19))==s.Rational(289,339738624)\nprint('PASS: exact all-n conformal action normalization; n19 coefficient289/339738624.')\n'''
if 'n19 coefficient289' not in t:t+=extra;p.write_text(t)
exec(compile(t,str(p),'exec'))