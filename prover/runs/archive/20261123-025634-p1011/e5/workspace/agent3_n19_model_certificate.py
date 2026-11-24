import sys;sys.path.insert(0,'workspace')
from agent4_translation_exact import translation_model
import sympy as S,numpy as np,json,math
from pathlib import Path
# Reuse only interval utilities, stopping before any certificate execution/write.
source=Path('workspace/agent4_translation_certificates.py').read_text()
exec(source.split('results=[]')[0])
n=19;d=3;m=n-1
G1,G2,G3=translation_model(n,d)
powers=S.Matrix(d+1,d+1,lambda i,j:2+2*i+2*j)
D=G2.multiply_elementwise(powers)
vq=S.Matrix([1,-S.Rational(469,1000),S.Rational(29,500),-S.Rational(1461,10**6)])
aa=S.Matrix([vq[j]*t**j for j in range(d+1)])
cp=S.expand((aa.T*D*aa)[0])
roots=np.roots([float(c)for c in S.Poly(cp,t).all_coeffs()]);root=min(z.real for z in roots if abs(z.imag)<1e-5 and z.real>0)
tl=S.Rational(math.floor(root*10**7),10**7);tu=tl+S.Rational(1,10**7)
assert interval(cp,tl,tl)[0]>0
assert interval(cp,tu,tu)[1]<0
assert interval(S.diff(cp,t),tl,tu)[1]<0
g=S.Matrix([aa[j]*(1+S.Rational(2*j,m+2))for j in range(d+1)])
b=S.Matrix([2*(j+1)*aa[j+1]for j in range(d)])
c=S.Matrix([2*(j+1)*(1+S.Rational(2*j,m+4))*aa[j+1] if j<d else 0 for j in range(d+1)])
C=(aa.T*G2*c)[0]
Hsupport=S.expand((m+2)*(g.T*G1*g)[0]+S.Rational(2*(m+1),(m+2)*(m+4))*(b.T*G3*b)[0]+3*C)
Htrans=S.expand(S.Rational(1,m+4)*(b.T*G3*b)[0]+C)
hs=interval(Hsupport,tl,tu);ht=interval(Htrans,tl,tu)
assert hs[1]<0 and ht[1]<0
print('CERTIFIED n19 MODEL strict minimum',list(vq),'root interval',tl,tu,'Hess upper',float(hs[1]),float(ht[1]))
result={'n':n,'vector':[str(z)for z in vq],'t_lower':str(tl),'t_upper':str(tu),'scale_derivative':str(cp),'Hsupport':str(Hsupport),'Htrans':str(Htrans),'claim':'MODEL ONLY: not a PDE example; discrepancy unresolved'}
Path('workspace/agent3_n19_model_certificate.json').write_text(json.dumps(result,indent=2))
import shutil,os
if os.path.abspath(__file__)!=os.path.abspath('workspace/agent3_n19_model_certificate.py'):shutil.copyfile(__file__,'workspace/agent3_n19_model_certificate.py')
