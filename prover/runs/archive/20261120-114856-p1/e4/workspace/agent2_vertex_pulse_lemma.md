# Exact negative-action pulse reflection at an (s+1)-node vertex

Let w be a positive s+1-node measure, q its monic degree-s OP, h=H, w'=w q^2/H, r the next OP. Then q_i r_i=H. Put f=(1,z,...,z^{s-1})^T, G=E_w ff^T, G'=E_w' ff^T, R=-(G')^{-1}G, and d=E_w[(r-q)f^T]. A coefficient perturbation v induces dq=f^T v, dr=f^T Rv and dh=dv. For a negative-level node beta satisfying q_beta r_beta=-H, define

C_beta=4 q_beta G^{-1} f_beta,
a_beta(v)=[r_beta f_beta^T v+q_beta f_beta^T Rv+dv]/H.

Both exact sign identities are

 dh(C_beta)=-4(H+q_beta^2)<0,
 a_beta(C_beta)=-4[K_G(beta,beta)+(q_beta^2/H)K_G'(beta,beta)+1+q_beta^2/H]<0.

Here K_G(x,x)=f_x^T G^{-1} f_x, and likewise for G'. The first follows from d G^{-1}=coeff(r-q)^T. The second follows by multiplying out C, using R G^{-1}=-(G')^{-1} and q_beta r_beta=-H. No approximate quadrature or root calculation is involved.

In the leading pulse ODE vdot=-C_beta eta, etadot=-2 a_beta(v) eta, set a=a_beta(v), c=a_beta(C_beta)<0. Then adot=-c eta and a^2-c eta is conserved. The complete pulse from eta=0,a_in<0 to eta=0,a_out>0 has a_out=-a_in and

 v_out = [I-2 C_beta a_beta/c] v_in.

This is an involutive reflection. For the positive norm deficit D(v)=-dh(v), put kappa=dh(C_beta)/a_beta(C_beta)>0. Then D+kappa*a is constant during a pulse and D_out=D_in+2*kappa*a_in < D_in. A physically admissible full reflection with D_out>0 therefore needs -D_in/(2*kappa)<a_in<0.

This lemma does NOT establish that the full restarted-CG orbit is asymptotic to a sequence of such pulses, nor does deficit decrease alone exclude an infinite contracting reflection/edge cycle. Those are separate global dynamical questions.
