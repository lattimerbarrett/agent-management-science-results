# Dimension-four Green expansion at an umbilic boundary point

Assume n=4, positive Robin Yamabe type, local conformal flatness, and II°(p)=0. This proves a local Green expansion and identifies its AF mass. It does not show that an arbitrary nonlinear blowup point is umbilic, isolated, or simple.

## Flat normalization

Conformally flatten the metric nearp. A local Möbius factor can adjust the mean curvature atp while retaining flatness; since II°(p)=0, arrange II(p)=0. In flat graph coordinates the boundary is t=f3(z)+O(|z|4), with z∈R3, domain above the graph, and f3 homogeneous cubic. Write uniquely f3=H3+|z|²L1, with H3 harmonic cubic and L1 linear. Then Δf3=10L1.

The boundary operator is B=∂out+H/3. Direct graph expansion gives

B(r^−2)=−4f3/r4+(Δf3)/(3r²)+O(1).

Thus the homogeneous-degree0 correction q must be harmonic and satisfy

∂out q=4H3/r4+(2/3)L1/r² on t0.

## Exact angular correction

Write q=q(ω) on S³_+. Then Δ_{S³}q=0 with the above angular boundary data. These data are odd in z, so have zero boundary mean. The angular Neumann problem therefore has a unique odd solution (the otherwise free constant is fixed by oddness). Its boundary degree1 and3 Dirichlet-to-Neumann multipliers are respectively4/π and32/(3π). Consequently

q(z,0)=(3π/8)H3(z)/|z|3+(π/6)L1(z)/|z|.

The angular solution is smooth up to the hemisphere boundary, analytic locally through the equator, and odd under z↦−z. In particular its hemisphere average is zero. All multiplier/source constants are checked in agent4_n4_log_checks.py.

## Parametrix and regular remainder

Take a cutoff of G0=r^−2+q nearp. It is harmonic offp in the flat patch, including the thin part below the tangent plane after analytic continuation. On the actual curved boundary, B G0=O(1): the leading degree−1 defect cancels by construction; the quartic boundary Taylor term gives a bounded residual; geometric changes in q contribute only O(r). Away fromp all cutoff errors are smooth.

Invert the global coercive Robin form to correct these bounded boundary and smooth interior errors. Standard Robin W^{1,p} regularity gives the correction in W^{1,p} for every finitep, hence C^{0,α} for everyα<1. The result is the positive Green function with normalized leading coefficient1,

G=r^−2+q(ω)+A+O(r^α).

Annular boundary estimates give gradient remainderO(r^{α−1}). Positivity follows by applying the coercive-form negative-part argument away from a tiny ball, whose inner boundary value is positive.

## AF geometry and mass

The Green metric ĝ=G²g is complete, scalar-flat and minimal-boundary offp. Under inversion y=x/r², R=|y|,

ĝ=[1+(A+q(ω))/R²+O(R^{−2−α})]²δ.

The boundary is a graph y_n=b(y')+O(R^−2), with b=f3(y')/|y'|4 homogeneous degree−1 and odd. Thus flattening its end changes coordinates by a degree−1 vector field V with only normal leading component, odd in y'. Its metric gauge term has tangential-normal coefficients even and normal-normal coefficient odd in y'. Every bulk ADM flux of this gauge is odd after contraction with the radial normal, and the boundary correction integrand is odd as well; both integrate to zero. The q contribution is zero because its hemisphere average is zero. The remaining mass is a strictly positive conventional factor timesA.

The decay order is2>(4−2)/2=1; scalar curvature and boundary mean curvature vanish, so the usual noncompact-boundary positive mass theorem in dimension4 applies (or after taking the orientable cover if needed). It gives A>=0, and rigidity gives A=0 only for the Euclidean halfspace Green metric. Compactification and local conformal rigidity then identify the original manifold with the conformal round hemisphere. Under the problem's exclusion, therefore A>0.

This last paragraph explicitly invokes the standard boundary positive mass theorem, not a newly proved theorem. It is the terminal global mass step only; all nonlinear blowup selection and sign estimates remain separate.
