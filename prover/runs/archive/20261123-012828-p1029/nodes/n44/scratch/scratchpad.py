from pathlib import Path
p=Path('experiments/e1/agent3_completion_audit.md')
print(p.read_text() if p.exists() else 'No completion audit present')
import sympy as s
h,C=s.symbols('h C', real=True)
print('\nScalar identity behind the functional-calculus estimate:')
print(s.factor(C*h-h**2))
print('For 0 <= h <= C: h^2 <= C h. Hence tau(h^2) <= C tau(h).')
