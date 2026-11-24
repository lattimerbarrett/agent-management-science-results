import sympy as s
P=4*s.pi
# Two geometric trajectories, each with all possible sphere recappings.
actions0=[-k*P for k in range(-1,3)]
actions1=[-P/2-k*P for k in range(-1,3)]
print('First geometric orbit actions:',actions0)
print('Second geometric orbit actions:',actions1)
c_unit=0;c_A=-P/2;c_point=-P
print('Three strictly decreasing selectors:',c_unit,c_A,c_point)
print('These use only two geometric orbits: first, second, first recapped.')
print('Quantum-square selector inequality:',bool(c_unit-P<c_A<c_unit))
print('With only ONE orbit all spectral values lie in a single coset modulo 4*pi; no value is strictly between c(unit)-4*pi and c(unit).')
