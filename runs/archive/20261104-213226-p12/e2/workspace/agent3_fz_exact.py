from fractions import Fraction
from sage.all import matrix,QQ
s=open('workspace/agent2_fz.py').read().split('base={}; pivots=[]')[0]
s=s.replace('def inv(x):return pow(x,P-2,P)','def inv(x):return Fraction(1,x)')
s=s.replace('pow(-logA[n],j,P)','(-logA[n])**j').replace('%P','')
exec(s)
assert matrix(QQ,rows).rank()==33
print('Exact FZ matrix rank = 33')
import pickle
pickle.dump((cols,rows,labels),open('workspace/agent3_fz_QQ.pkl','wb'))
