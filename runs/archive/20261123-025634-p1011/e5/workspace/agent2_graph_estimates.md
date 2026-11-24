# Local graph estimates (independent of global gluing)

Let m=n-1, D>=2, n>2D, and h_R=h(x)chi(x/R), where h is a fixed degree-D polynomial and chi is a fixed smooth compactly supported radial cutoff equal1 near0. All constants below are uniform R>=1. Derivative bounds |D^j h_R|<=C(1+r)^(D-j), j=0,1,2 hold. Let |t|(1+R)^(D-1)<=s<<1. Write U=(1+r²+z²)^(-(n-2)/2), U_t=U(x,t h_R(x)). The domain is z>t h_R.

The outward normal is (t Dh_R,-1)/(1+t²|Dh_R|²)^(1/2), and trace mean curvature is
 H=t Delta h_R/(1+t²|Dh_R|²)^(1/2)-t³ Hess h_R(Dh_R,Dh_R)/(1+t²|Dh_R|²)^(3/2).
Consequently its exact Robin residual is
 B U=(n-2)t U_t[(h_R-x.Dh_R)/((1+r²+t²h_R²)(1+t²|Dh_R|²)^(1/2))+Delta h_R/(2m(1+t²|Dh_R|²)^(1/2))-t² Hess h_R(Dh_R,Dh_R)/(2m(1+t²|Dh_R|²)^(3/2))].
The linear term is
 A_h=(n-2)(1+r²)^(-(n-2)/2)[(h-x.Dh)/(1+r²)+Delta h/(2m)].
Using |t h_R|/(1+r)<=Cs and |t Dh_R|<=Cs gives pointwise
 |t^(-1)BU-A_(h_R)|<=Cs²(1+r)^(D-n).
The envelope belongs to L^{2m/n}(R^m), because its radial exponent is
 2m(D-n)/n+m-1<-1 iff n>2D.
Therefore ||BU-t A_h||_(L^{2m/n})<=o_R(t)+Cs²|t|. Surface measures of the graph and plane are uniformly comparable, so the critical trace theorem turns this into the same bound in the dual energy norm.

For the energy J=1/2 int |grad U|²+c_n int H U²-(n-2)²/2 int U^{2n/(n-2)}, put e(U)=1/2|grad U|²-(n-2)²/2 U^q. Exact graph integration gives
 J_t(U)-J_0(U)=-int_Rm int_0^(t h_R) e(U)(x,z) dz dx+c_n t int_Rm [Delta h_R-t² Hess h_R(Dh_R,Dh_R)/(1+t²|Dh_R|²)] U_t² dx.
At z0, e(U)=c_n Delta_x(U²), so the t coefficient vanishes by integration by parts. All expressions are odd in t, hence the second coefficient vanishes as well. More quantitatively, |partial_z² e(U)|<=C(1+r)^(-2n) for |z|<=s(1+r), and |U_t²-U_0²|<=Ct²h_R²(1+r)^(-2)U_0². Each remaining bulk or boundary term is bounded by
 C|t|³ int_0^(CR) (1+r)^(3D-n-2)dr
 <=Cs t² int_0^infty (1+r)^(2D-n-1)dr <=C' s t²,
again exactly under n>2D. Thus J_t(U)=J_0(U)+O(s t²), uniformly R.

These are LOCAL graph estimates only. They do not themselves prove the complete compact-manifold Lyapunov–Schmidt expansion or the requested dimension classification. In particular they do not explain why an n19,D8 finite-dimensional strict minimum should fail to yield a PDE example.
