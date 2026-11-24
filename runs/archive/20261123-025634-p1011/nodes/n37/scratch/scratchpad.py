import sympy as s
from fractions import Fraction
# Reproduce the diagonal checks without the source's self-copy/write operation.
source=open('experiments/e1/agent2_diagonal_checks.py').read()
source=source[:source.index("Path('workspace/")]
exec(compile(source,'agent2_diagonal_checks_readonly','exec'))
print('\nSequential single-patch scaling with amplitude mu=epsilon^8:')
for N in [19,20,21,22,23,24,25,40,100]:
 residual_power=s.Rational(N-2,2)-8
 background_energy_power=N-2-16
 cubic_power=24-max(23-N,0)-16
 assert residual_power>0 and background_energy_power>0 and cubic_power>0
 print('n=%d: residual/mu = O(eps^%s), background/mu^2 = O(eps^%s), cubic/mu^2 exponent >= %s'%(N,residual_power,background_energy_power,cubic_power))
print('\nBarrier check: if old boundary gap is gamma and sup energy change < gamma/4, the new gap is > gamma/2.')
