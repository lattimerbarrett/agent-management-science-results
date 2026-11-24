from fractions import Fraction
n=19
p=Fraction(n+2,n-2)
q=p+1
print('n=',n,'p=',p,'energy exponent q=',q)
print('p-2=',p-2,'q-2=',q-2)
print('At a=0 the nonlinear equation remainder is b^p, not O(b^2) uniformly:')
for b in [1e-2,1e-4,1e-8,1e-16]:
 print('b=',b,'N(0,b)/b^2=',b**float(p-2),'energy remainder/b^2=',b**float(q-2))
print('Valid uniform remainder orders: equation O(||w||^p), energy O(||w||^(p+1)).')
from pathlib import Path
p0=Path('experiments/e3/agent3_local_pohozaev_bridge.md')
text=p0.read_text()
start=text.index('## Step 4')
end=text.index('## Step 5') if '## Step 5' in text else start+11000
print('\nLOCAL REMAINDER STEP\n',text[start:end])
