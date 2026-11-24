def h0(a,b,e):
    return sum(max(b-i*e+1,0) for i in range(a+1)) if a>=0 else 0

def cohomology(a,b,e):
    h_0=h0(a,b,e)
    h_2=h0(-2-a,-e-2-b,e)
    chi=1+(-e*a*a+2*a*b-(e-2)*a+2*b)//2
    return h_0,h_0+h_2-chi,h_2
