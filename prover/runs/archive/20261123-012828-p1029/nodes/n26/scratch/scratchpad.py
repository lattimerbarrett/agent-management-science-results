from pathlib import Path
# Check the spectral-cutoff bounds, including noncommuting positive test increments.
p=Path('experiments/e1/agent2_threshold_checks.py')
exec(compile(p.read_text(),str(p),'exec'))
print('\nReduction: p_n=1_(eta/2,1](a_(n+1)-a_n) has')
print('tau(p_n)>=eta/(2-eta)>0 and sum_(n<N) p_n <= (2/eta)1.')
print('This is a Bessel projection configuration; the scalar bounds alone do not exclude it.')
print('For the original no-supremum sequence, the supplied verified exhaustion result directly forces eta=0.')
