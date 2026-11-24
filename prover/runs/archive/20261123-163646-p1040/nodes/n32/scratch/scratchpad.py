from pathlib import Path
# Execute the all-parameter algebra and field-polynomial checks without file writes.
p=Path('experiments/e2/agent3_stable_symbolic_checks.py')
s=p.read_text(); s=s[:s.index("Path('workspace/")]
exec(compile(s,str(p),'exec'))
# Independent quadratic critical-symbol checks in the first relevant local fields.
from sage.all import QQ, polygen, NumberField
xx=polygen(QQ)
for degree in [4,8,16]:
 d=degree//4
 K=NumberField(xx**(2*d)-2*xx**d+2,'pi'); pi=K.gen(); P=K.ideal(pi)
 print('c =',degree, ': critical quadratic symbol =',K.hilbert_symbol(1+pi,1+pi**(degree-1),P))
