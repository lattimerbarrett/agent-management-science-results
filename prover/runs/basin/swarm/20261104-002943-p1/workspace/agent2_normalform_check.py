import sympy as S

def check(s,x,P,H,w,h):
    # Exact rational second jet of the squared-residual map.
    n=len(x); V=S.Matrix([[z**j for j in range(s)] for z in x]); sig=S.Matrix([P(z)/H for z in x]); w=S.Matrix(w)
    assert all(z*z==1 for z in sig)
    assert V.T*S.diag(*w)*sig==S.zeros(s,1)
    M=V.T*S.diag(*w)*V; inv=M.inv(); hv=S.Matrix([h(z) for z in x]); E=(hv.T*S.diag(*w)*hv)[0]
    normal=S.Matrix([w[i]*sig[i]*hv[i] for i in range(n)])
    def jet(arr):
        m=[V.T*S.diag(*a)*V for a in arr]
        ai=[V.T*S.diag(*a)*sig for a in arr]
        c=[S.zeros(s,1)]*3
        c[0]=inv*ai[0]
        c[1]=inv*(ai[1]-m[1]*c[0])
        c[2]=inv*(ai[2]-m[1]*c[1]-m[2]*c[0])
        p=[sig-V*c[0],-V*c[1],-V*c[2]]
        raw=[S.zeros(n,1) for _ in range(3)]
        for k in range(3):
            for j in range(k+1):
                for a in range(k-j+1):
                    b=k-j-a
                    raw[k]+=S.Matrix([arr[j][i]*p[a][i]*p[b][i] for i in range(n)])
        den=[sum(v) for v in raw]; out=[]
        for k in range(3):
            z=raw[k]
            for j in range(k): z-=out[j]*den[k-j]
            out.append(z/den[0])
        return out
    zero=S.zeros(n,1)
    out=jet(jet([w,normal,zero]))
    assert out[0]==w and out[1]==normal
    k=V*inv*V.T*S.Matrix([w[i]*sig[i]*hv[i]**2 for i in range(n)])
    predicted=S.Matrix([2*w[i]*(E-hv[i]**2+sig[i]*k[i]) for i in range(n)])
    assert S.simplify(out[2]-predicted)==zero
    assert sum(predicted)==0
    assert V.T*S.diag(*sig)*predicted==S.zeros(s,1)
    print('s=',s,'exact second-jet identity checked; tangent drift=',list(predicted))

if __name__=='__main__':
    check(4,[-8,-7,-4,-1,1,4,7,8],lambda x:x**4-65*x*x+424,S.Integer(360),[S.Rational(1,8)]*8,lambda x:S.Rational(1,11)+x/S.Integer(7)+x*x/S.Integer(13)+x**3/S.Integer(101))
