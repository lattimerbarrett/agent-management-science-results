import sympy as s
eta,u,v=s.symbols('eta u v', real=True)
print('Endpoint constraints: eta <= u <= 1-eta')
print('At eta=1/2, interval endpoints:',s.Rational(1,2),1-s.Rational(1,2))
print('For 0<=a_n<a_(n+1), strict order preservation requires tau(a_n)<tau(a_(n+1)).')
print('So eta=1/2 is excluded.')
from pathlib import Path
p=Path('experiments/e1/agent3_qt_ultraproduct_notes.md')
print('\nUltraproduct construction available:',p.exists())
if p.exists(): print(p.read_text())
