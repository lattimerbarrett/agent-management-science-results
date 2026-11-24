from pathlib import Path
r=Path('experiments/e7')
print('Exists:',r.exists())
if r.exists():
 for p in r.iterdir():
  if p.is_file() and any(t in p.name.lower() for t in ['interact','cluster','n7','compactness_bridge']):
   print(p.name)
print('\nMulti-bubble interaction scaling audit:')
import sympy as s
x,y,d,n=s.symbols('epsilon_i epsilon_j d n',positive=True)
a=(n-2)/2
E=-(x*y)**a/d**(n-2)
print('E_pair =',E)
print('epsilon_i*dE_pair/d(epsilon_i) =',s.simplify(x*s.diff(E,x)))
print('Common-scale derivative =',s.simplify(x*s.diff(E,x)+y*s.diff(E,y)))
