import sympy as S

def block(lam,r,s):
    A=S.diag(*lam)
    K=S.Matrix.hstack(*[(A**j)*r for j in range(s)])
    if (K.T*A*K).det()==0: return S.zeros(len(lam),1)
    return r-A*K*(K.T*A*K).inv()*K.T*r

for lam,s in [([1,2,3,4,5],2),([1,2,3,5],2),([1,2,3,6],2),([1,2,4,5],2)]: 
    r=S.ones(len(lam),1);Ai=S.diag(*[1/S.Integer(x) for x in lam])
    factors=[]; efactors=[]
    for k in range(3):
        z=block(lam,r,s)
        factors.append(S.factor((z.T*z)[0]/(r.T*r)[0]))
        efactors.append(S.factor((z.T*Ai*z)[0]/(r.T*Ai*r)[0]))
        r=z
    print('spectrum',lam,'s',s)
    print('residual squared factors:',factors)
    print('energy squared factors:',efactors)
    print('successive energy differences:',[S.sign(efactors[i+1]-efactors[i]) for i in range(2)])
    print('successive residual differences:',[S.sign(factors[i+1]-factors[i]) for i in range(2)])
