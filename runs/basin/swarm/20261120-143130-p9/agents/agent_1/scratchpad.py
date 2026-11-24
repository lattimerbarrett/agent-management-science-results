import mpmath as mp
mp.mp.dps = 50

def Ap_interval(p, a, b, alpha):
    def integral_power(r):
        if a >= 0:
            return (b**(r+1)-a**(r+1))/(r+1)
        if b <= 0:
            return ((-a)**(r+1)-(-b)**(r+1))/(r+1)
        return ((-a)**(r+1)+b**(r+1))/(r+1)
    return integral_power(alpha)/(b-a)*(integral_power(-alpha/(p-1))/(b-a))**(p-1)

count=0
for p in map(mp.mpf, ['1.25','1.5','2','3','5']):
    for eps in map(mp.mpf, ['0.2','0.1','0.03']):
        for alpha in [(p-1)*(1-eps), -1+eps]:
            D=(alpha+1)*(1-alpha/(p-1))**(p-1)
            assert mp.almosteq(Ap_interval(p,mp.mpf(0),mp.mpf(1),alpha),1/D)
            for a,b in [('-2','-1'),('-1','0.3'),('0','1'),('0.01','1'),('0.8','1'),('-0.7','4')]:
                value=Ap_interval(p,mp.mpf(a),mp.mpf(b),alpha)
                assert value <= 2**p/D*(1+mp.mpf('1e-45'))
                count+=1
        # H[y^(-1+eps) 1_(0,1)](-t), integrated in two pieces.
        # The change y=t*u^(1/eps) removes the singularity at zero.
        for t in map(mp.mpf,['0.01','0.2','0.8']):
            first=t**(eps-1)/eps*mp.quad(lambda u: 1/(1+u**(1/eps)),[0,1])
            rest=mp.quad(lambda y:y**(eps-1)/(t+y),[t,1])
            Habs=(first+rest)/mp.pi
            assert Habs >= t**(eps-1)/(2*mp.pi*eps)
            count+=1
        # Exact H of 1_(0,1) at x=exp(-1/eps).
        x=mp.exp(-1/eps)
        Habs=mp.log((1-x)/x)/mp.pi
        assert Habs >= 1/(2*mp.pi*eps)
        count+=1
print(f'{count} finite numerical checks passed (not a proof of the general assertions).')
