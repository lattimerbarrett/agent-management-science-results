from pathlib import Path
p=Path('workspace/agent4_edgeworth.py');s=p.read_text();needle="V=S.hessian(Ls[2],t);Cov=V.inv()";repl="""# Compact centered derivative table, checked as an exact polynomial identity.
mean=sum(xx)/r;center=[x-mean for x in xx]
S2=sum(x*x for x in center);S3=sum(x**3 for x in center);S4=sum(x**4 for x in center)
assert S.expand(Ls[2]-S2/16)==0
assert S.expand(Ls[3]+S3/192)==0
assert S.expand(Ls[4]+S.Rational(5,768)*S4-S2**2/512)==0
V=S.hessian(Ls[2],t);Cov=V.inv()""";assert needle in s;s=s.replace(needle,repl);p.write_text(s)
import sys
sys.path.insert(0,'workspace')
exec(s)
