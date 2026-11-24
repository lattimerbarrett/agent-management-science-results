import mpmath as mp
mp.mp.dps=70
# Compare the interval characteristic with the arithmetic-average matrix expression.
# Two equally likely matrices R(+theta/2)diag(M,1)R^T and R(-theta/2)diag(M,1)R^T.
for p in [mp.mpf('1.5'),mp.mpf(2),mp.mpf(4)]:
    q=p/(p-1)
    print('p=',float(p))
    for logM in [8,16,32]:
        M=mp.mpf(10)**logM
        theta=M**(-1/p)
        t=M**(1/p)
        # Frobenius norm squared of diag(t,1)R(theta)diag(1/t,1), determinant 1.
        S=2*mp.cos(theta)**2+(t*t+1/(t*t))*mp.sin(theta)**2
        K=mp.sqrt((S+mp.sqrt(S*S-4))/2)
        true_root=((1+K**q)/2)**(1/q)
        c=mp.cos(theta/2)**2; s=mp.sin(theta/2)**2
        avW=[M*c+s,M*s+c]
        b=M**(-1/(p-1))
        avB=[b*c+s,b*s+c]
        arithmetic=max(avW[j]**(1/p)*avB[j]**(1/q) for j in range(2))
        print(' log10 M=',logM,' true root=',mp.nstr(true_root,8),' arithmetic=',mp.nstr(arithmetic,8),' ratio=',mp.nstr(arithmetic/true_root,8))
