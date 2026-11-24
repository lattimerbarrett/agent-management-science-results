# Independent exact graph-flux normalization audit

This checks the exact identity in agent3's full SP7 audit, without asserting the unassembled SP7 estimate.

For a domain above a graph t=F(z), its outward normal is (DF,-1)/sqrt(1+|DF|²). Put S=z·DF-F and T=H sqrt(1+|DF|²)=∆F-F_a F_b F_ab/(1+|DF|²), beta=(n-2)/(2(n-1)), a=(n-2)/2, κ=n(n-2)/q=(n-2)²/2. Robin gives u_ν dσ=-beta T u dz. Thus the exact graph contribution to the critical Pohozaev flux is

    I=-beta T u(z·∇_z u+F u_t+a u)-(S/2)|∇u|²+κ S u^q,

where every ambient derivative is evaluated at t=F. In particular ∇_z is NOT differentiation of the restricted trace u(z,F(z)). The round-sphere flux P is minus the integral of I.

For a radial bubble U=(1+r²)^(-(n-2)/2), replacing F by -F keeps U, |∇U|², U^q and z·∇_z U+F U_t unchanged and changes S,T to their negatives. The projected cap { |z|²+F(z)²<R² } is unchanged. Hence the complete direct-bubble graph integral is odd under F↦-F. This includes the moving cap and proves all its even shape coefficients vanish, not just a formal bulk coefficient.

For F=f_j homogeneous of degree j, let I_j=integral_(S^(n-2)) f_j. Angular integration gives integral ∆f_j=j(j+n-3)r^(j-2)I_j. With V=U², the linear radial density is

    r^(n-2){-beta j(j+n-3)r^(j-2)[rV'/2+aV]
      -2a²(j-1)r^(j+2)V/(1+r²)²
      +2a²(j-1)r^j V/(1+r²)²} I_j.

It is exactly the radial derivative of

    c_n[-(j-1)r^(j+n-2)V'-j(n-2)r^(j+n-3)V] I_j.

The lower endpoint is zero for j>=2,n>=3. At large r, its coefficient at r^(j+1-n) is

    (n-2)²(j-2)/(4(n-1)) I_j.

**Sign bookkeeping:** this is the sign of integral I, not of P=-integral I. Consequently raw P has the negative coefficient, and the adapted P adds the positive coefficient, exactly as used in the n5,n6,n7 mass tables.

`agent1_exact_graph_flux_checks.py` differentiates and simplifies the complete rational radial formula exactly for n=3,...,10 and j=2,...,8, verifies all 56 lower endpoints and all 56 asymptotic coefficients, and checks the formal outward-normal algebra. It ran successfully. The finite collection corroborates the displayed derivation; it does not alone certify a dimension-uniform theorem or the full nonlinear stress estimate.
