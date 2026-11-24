from pathlib import Path
code='''from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
Q=[Fraction(-1),Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1),Fraction(2)]
Fs=[frozenset(c) for k in range(3) for c in combinations(range(len(Q)),k)]
rules=[]
for k in range(3):
 for c in combinations(Fs,k): rules.append(c)
checks=0
for ruleset in rules:
 thresholds=[Fraction(2)]
 for F in ruleset:
  thresholds.append(max(Q[i] for i in F) if F else Fraction(-1))
 alpha=min(thresholds)
 for r in [Fraction(j,20) for j in range(1,20)]:
  S={i for i,q in enumerate(Q) if q<r}
  output=any(F<=S for F in ruleset)
  assert output==(alpha<r)
  if r!=alpha:
   assert (not output)==(r<alpha)
  checks+=1
out={'threshold_checks':checks,'rule_families':len(rules),'rational_points':19,'scope':'Finite verification of monotone finite-set rule to infimum-threshold identity, not proof of infinite computability theorem.'}
Path('workspace/agent3_cut_checks.json').write_text(json.dumps(out,indent=2))
print(out)
'''
Path('workspace/agent3_cut_checks.py').write_text(code)
exec(compile(code,'workspace/agent3_cut_checks.py','exec'),{})
# Check the exact invocation that previously caused recursion, twice.
import runpy
runpy.run_path('workspace/agent3_cut_checks.py')
runpy.run_path('workspace/agent3_cut_checks.py')
assert Path('workspace/agent3_cut_checks.py').read_text()==code
print('Restored safely; repeated runpy calls leave script unchanged.')