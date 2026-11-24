from fractions import Fraction
import builtins,time
class Exact:
 def __rmod__(self,a):return Fraction(a)
def qpow(a,b,m=None):return Fraction(a)**b
src=open('workspace/agent3_fz25.py').read()
src=src.replace('P=1000000007; N=12; g=25','P=Exact(); N=12; g=25\npow=qpow')
src=src[:src.index('json.dump(dict')]
startclock=time.time();exec(src)
print('exact rational time',time.time()-startclock)
assert rank==33
