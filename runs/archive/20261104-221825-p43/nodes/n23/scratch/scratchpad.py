import sympy as s
m,k=s.symbols('m k',integer=True)
area=4*s.pi*(m+k)
c1=2*(m+k)
print('area - 2*pi*c1 =',s.simplify(area-2*s.pi*c1))
n=2; N=s.gcd(2,2)
print('dimension =',2*n,'; minimal Chern number =',N,'; N >= n:',N>=n)
print('sphere area group = 4*pi*Z (rational)')
# Positive-degree cohomology generators a,b have a^2=b^2=0.
def mul(p,q):
    out={}
    for (i,j),v in p.items():
        for (k,l),w in q.items():
            if i+k<=1 and j+l<=1:
                out[i+k,j+l]=out.get((i+k,j+l),0)+v*w
    return {ij:v%2 for ij,v in out.items() if v%2}
a={(1,0):1}; b={(0,1):1}
print('a*b =',mul(a,b),' a*a =',mul(a,a),' b*b =',mul(b,b))
print('Every triple positive-degree product has degree >= 6 > 4; cup-length = 2; lower bound = 3.')
