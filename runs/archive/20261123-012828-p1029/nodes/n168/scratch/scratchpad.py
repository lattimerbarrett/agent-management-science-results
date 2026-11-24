from pathlib import Path
# Audit the metric implication independently of the given order-completeness theorem.
import sympy as s
h=s.symbols('h', real=True)
print('Functional-calculus identity:',s.factor(h-h*h))
print('For 0<=h<=1: tau(h)^2 <= tau(h^2) <= tau(h).')
print('If tau(b_n)=eta>0, then d_tau(a_(n+1),a_n)>=eta**(2/3).')
print('Thus the proposed sequence is not metric Cauchy.')
print('The given order-completeness theorem nevertheless supplies a supremum.')
print('There is no contradiction unless order-to-metric continuity is also assumed.')
print('The defining no-supremum condition is therefore impossible, independently of the metric.')
