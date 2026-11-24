import math
# Random incidence construction: N=1024*t, |B_i|=q,
# lambda=q^2/N, d=floor(q/64), h=floor(lambda/8).
# Three union bounds, all in logarithmic form.
for t in [10**12,10**16,10**24]:
 N=1024*t
 q=math.ceil(math.sqrt(10**6*N*math.log(t)))
 lam=q*q/N; d=q//64; h=int(lam//8)
 log_pair=2*math.log(t)-lam/8
 # For a fixed D of size at most d, P(|B_i intersect D|>=h).
 log_p=h*math.log(math.e*(q*d/N)/h)
 log_badD=(d+1)*math.log(N+1)+q*math.log(t)+q*log_p
 # Sum over |S|=s and s+1 exceptional groups is a geometric sum.
 log_ratio=math.log(N*t)-q/128
 log_cover=log_ratio-math.log1p(-math.exp(log_ratio)) if log_ratio<0 else float('inf')
 print('t=',t,'q=',q,'R=',2*q,'b upper=',2*t*q)
 print('log failure bounds:',log_pair,log_badD,log_cover)
 print('effective upper exponent',math.log(2*t*q)/math.log(t))
