"""Run the independently written FZ generator over exact rational coefficients."""
from pathlib import Path
s=Path(__file__).with_name('fz25_agent2.py').read_text()
s=s.replace('P=1000000007', """from fractions import Fraction
class RationalMod:
    def __rmod__(self,x): return Fraction(x)
    def __str__(self): return 'QQ'
P=RationalMod()
def pow(a,b,p): return Fraction(a)**b""")
exec(compile(s,'fz25_rational.py','exec'))
