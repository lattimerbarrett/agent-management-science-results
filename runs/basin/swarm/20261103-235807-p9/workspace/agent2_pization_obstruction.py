import math

def power_average(alpha,R):
    if abs(alpha+1)<1e-12: return math.log1p(R)/R
    return math.expm1((alpha+1)*math.log1p(R))/((alpha+1)*R)

def normalized_pization_characteristic_on_interval(p,a,R):
    # Second scalar diagonal entry of normalized pization, on [0,R].
    return power_average(-a*(p-1),R)*power_average(a,R)**(p-1)

if __name__=='__main__':
    for p,a in ((3,.75),(4,.6),(6,.4)):
        exponent=a*(p-1)-1
        assert exponent>0
        rows=[]
        for R in (1e2,1e4,1e8,1e16):
            Ap=normalized_pization_characteristic_on_interval(p,a,R)
            rows.append((R,Ap,Ap/R**exponent))
        target=1/((a*(p-1)-1)*(a+1)**(p-1))
        assert abs(rows[-1][2]/target-1)<.001
        print('p,a,divergence exponent=',p,a,exponent,'asymptotic constant=',target)
        print(rows)
