"""Exact inequalities supporting the flat critical-arc collapse lemma."""
import sympy as s
from sage.all import RealIntervalField, QQ
R=RealIntervalField(100)
# Uniform in 0<delta<=1/8 and transition s>=1-delta/4:
# Aouter-Acore >=delta*(3/4-delta/4-exp(-1)) > delta/3.
margin=R(3)/4-R(1)/32-(-R(1)).exp()-R(1)/3
assert margin.lower()>0
print('Uniform positive A-axis gap/delta minus1/3:',margin)
# Bouter-Bcore=delta*(s-exp(-1/s²))>0 for 0<s<=1:
# log(s)+1/s² decreases on (0,1], with value1 at1.
u=s.symbols('u',positive=True)
assert s.simplify(s.diff(s.log(u)+1/u**2,u)-(u*u-2)/u**3)==0
print('B-axis gap positive by exact derivative sign on (0,1]')
# Every radial function with positive axes has a unique ellipsoid level:
# d/ds[(X/A)^2+|Y|²/B²] is strictly negative off the origin.
A,B,Ap,Bp,X,Y=s.symbols('A B Ap Bp X Y',positive=True)
level_derivative=-2*X**2*Ap/A**3-2*Y**2*Bp/B**3
assert level_derivative.is_negative
print('Nested ellipsoid uniqueness: exact derivative negative')
