from fractions import Fraction
from sage.all import matrix,QQ
for G in [24,25,26]:
 s=open('workspace/agent2_fz.py').read().split('base={}; pivots=[]')[0]
 s=s.replace('k0=48',f'k0={2*G-2}').replace('range(1,11)','range(1,D+1)')
 s=s.replace('range(9,13)','range(1,D+1)').replace('3*r-26+1',f'3*r-{G+1}+1').replace('(size-r)%2',f'({G}-r-size-1)%2')
 s=s.replace('def inv(x):return pow(x,P-2,P)','def inv(x):return Fraction(1,x)').replace('pow(-logA[n],j,P)','(-logA[n])**j').replace('%P','')
 scope={'Fraction':Fraction};exec(s,scope)
 U=matrix(QQ,scope['rows']).rank()
 print('GENUS',G,'upper relation rank',U,'quotient',77-U)
 # generate exact pairing using the same multiset Bell recurrence
 lower=open('workspace/agent3_lower.py').read()
 funcs=lower[lower.index('from fractions import Fraction'):lower.index("t=time.time(); E=")]
 lowerprefix=lower[:lower.index('weights=')]
 scope2={};exec(lowerprefix,scope2)
 funcs=funcs.replace('factorial(47+k)',f'factorial({2*G-3}+k)').replace('range(24)',f'range({G-1})')
 exec(funcs,scope2)
 part=scope2['partitions'];integ=scope2['exact_integral']
 E=[[integ(tuple(sorted(a+b,reverse=True))) for b in part(G-14)] for a in part(12)]
 print('GENUS',G,'exact pairing rank',matrix(QQ,E).rank())
