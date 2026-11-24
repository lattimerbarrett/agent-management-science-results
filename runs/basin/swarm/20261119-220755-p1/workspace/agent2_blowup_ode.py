import numpy as np

class BlowupODE:
    def __init__(self,nodes,f,g,N,mus):
        self.nodes=np.asarray(nodes,float);self.f=np.asarray(f,float);self.g=np.asarray(g,float);self.N=float(N);self.mus=np.asarray(mus,float)
        self.s=len(f)-1;self.t=len(nodes)-self.s-1
        self.d=np.array([np.prod([a-b for b in nodes if a!=b]) for a in nodes])
        self.V=np.array([self.nodes**j for j in range(self.s)]).T
        self.Vh=np.array([self.nodes**j for j in range(self.t)]).T
        self.Vmu=np.array([self.mus**j for j in range(self.s)]).T
        self.fv=np.polynomial.polynomial.polyval(self.nodes,self.f);self.gv=np.polynomial.polynomial.polyval(self.nodes,self.g)
        self.fm=np.polynomial.polynomial.polyval(self.mus,self.f);self.gm=np.polynomial.polynomial.polyval(self.mus,self.g)
    def __call__(self,time,state,logtime=True):
        t,s=self.t,self.s;h=np.r_[state[:t],1.];w=state[t:t+s];Z=state[t+s:]
        H=np.polynomial.polynomial.polyval(self.nodes,h);wv=self.V@w
        p=self.N*H/(self.d*self.fv);pp=H*self.fv/self.d
        M=self.V.T@(p[:,None]*self.V);Mp=self.V.T@(pp[:,None]*self.V)
        dg=np.linalg.solve(Mp,-self.V.T@((H*wv/self.d)*self.gv))
        dN=self.N**2*np.sum(H*wv/(self.d*self.fv**2))
        dhv=H*(self.gv*wv+self.fv*(self.V@dg)-dN)/self.N
        dh=np.linalg.lstsq(self.Vh,dhv,rcond=None)[0]
        if np.max(abs(self.Vh@dh-dhv))>1e-6*(1+np.max(abs(dhv))):raise ArithmeticError('dual interpolation failure')
        ratio=(self.gv*wv+self.fv*(self.V@dg)-dN)/self.N
        wf=-np.linalg.solve(M,self.V.T@(p*self.fv*ratio**2))
        if len(Z):wf-=4*np.linalg.solve(M,self.Vmu.T@(Z*self.fm))
        growth=2*((self.Vmu@w)/self.fm+(self.Vmu@dg)/self.gm)-2*dN/self.N
        if logtime:return np.r_[2*dh,w+wf,Z*(2+growth)]
        return np.r_[2*dh,wf,Z*growth]

def rational_s4():
    f=np.array([1377/1400,0.,-91/10,0.,1.]);g=np.array([4797/1400,0.,-49/10,0.,1.]);N=f[0]*g[0]
    prod=np.polynomial.polynomial.polymul(f,g);prod[0]+=N
    roots=np.roots(prod[::-1]);mus=np.sort(roots.real[(abs(roots.imag)<1e-8)&(roots.real>0)&(roots.real<1)])
    return BlowupODE(np.arange(-3.,4.),f,g,N,mus[:1])

if __name__=='__main__':
    ob=rational_s4();print('central negative modes',ob.mus,'N',ob.N)
    state=np.r_[[-2.25,0.],[.03,-.02,.015,.01],[.001]]
    print('field',ob(0,state,False))
    def op(p,nodes,s):
        V=np.array([nodes**j for j in range(s)]).T;M=V.T@(p[:,None]*V)
        coef=np.linalg.solve(M,-V.T@(p*nodes**s));fv=nodes**s+V@coef;N=np.dot(p,fv*fv)
        return coef,N,p*fv*fv/N
    nodes=np.r_[ob.nodes,ob.mus]
    for eps in [1e-3,3e-4,1e-4]:
        h=np.r_[state[:ob.t],1.];fp=ob.f.copy();fp[:ob.s]+=eps*state[ob.t:ob.t+ob.s]
        H=np.polynomial.polynomial.polyval(ob.nodes,h);F=np.polynomial.polynomial.polyval(ob.nodes,fp)
        pbase=H/(ob.d*F);pbase/=pbase.sum();ext=eps**2*state[ob.t+ob.s:];p=np.r_[pbase*(1-ext.sum()),ext]
        pp=op(op(p,nodes,ob.s)[2],nodes,ob.s)[2];bp=pp[:len(ob.nodes)];bp/=bp.sum()
        fc,NN,_=op(bp,ob.nodes,ob.s);hf=ob.d*bp*(ob.nodes**ob.s+ob.V@fc)/NN
        hc=np.linalg.lstsq(np.column_stack([ob.Vh,ob.nodes**ob.t]),hf,rcond=None)[0][:-1]
        estimate=np.r_[(hc-state[:ob.t])/eps,(fc-fp[:-1])/eps**2,(pp[len(ob.nodes):]-ext)/eps**3]
        print('eps',eps,'estimate',estimate,'err',estimate-ob(0,state,False))
