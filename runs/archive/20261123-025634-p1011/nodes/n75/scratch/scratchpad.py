from pathlib import Path
import sympy as s
n=s.symbols('n', integer=True, positive=True)
c=(n-2)/(4*(n-1));p=(n+2)/(n-2)
k=2**((n-2)/2)
print('Original scalar curvature:',s.simplify(n*(n-2)/c))
print('For v=k*u, k=2^((n-2)/2):')
print('nonlinear coefficient =',s.simplify(n*(n-2)*k**(1-p)))
print('resulting scalar curvature =',s.simplify(n*(n-2)*k**(1-p)/c))
print('boundary covariance: H_new = [1/(2*c)] u^(-n/(n-2)) B_g u')
print('1/(2*c) =',s.simplify(1/(2*c)))
print('\nAll Markdown/text filenames mentioning compactness and umbilicity:')
for root in ['experiments/e1','experiments/e7']:
    for f in Path(root).glob('*'):
        if f.is_file() and f.suffix in ['.md','.txt']:
            t=f.read_text(errors='replace').lower()
            if 'compactness' in t and 'umbilic' in t:
                print(f)
