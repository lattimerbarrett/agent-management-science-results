from pathlib import Path
import ast
src=Path('workspace/agent3_seed19_alln_checks.py').read_text()
# Execute source as authored (does not write teammate files), then strengthen
# endpoint coefficient certificate to exclude a vanishing polynomial at n=29.
ns={}
exec(compile(src,'workspace/agent3_seed19_alln_checks.py','exec'),ns)
s=ns['s'];n=ns['n'];t=ns['t'];U=ns['U']
for name,e in ns['checks'].items():
 for tv in (0,U):
  val=s.factor(e.subs(t,tv).subs(n,29))
  assert val.is_Rational and val>0,(name,tv,val)
print('Independent audit: all 16 endpoint certificates strictly positive at n=29 too.')
Path('workspace/agent2_audit_seed19_alln.py').write_text(Path(__file__).read_text())
