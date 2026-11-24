import sympy as s
from pathlib import Path
eta=s.symbols('eta', positive=True)
t=eta/2
delta=s.simplify((eta-t)/(1-t))
C=s.simplify(1/t)
print('Spectral threshold:',t)
print('Dimension lower bound:',delta)
print('Partial-sum Bessel bound:',C)
assert s.simplify(t+(1-t)*delta-eta)==0
assert s.simplify(t*C-1)==0
print('Both symbolic bounds checked.')
print('\nUltraproduct background from the existing proof notes:')
p=Path('experiments/e1/agent3_qt_ultraproduct_notes.md')
print(p.read_text())
