# Dimension-five Green mass at an umbilic boundary point

This supplies the GM input for n5 after the local Pohozaev calculation forces II°(p)=0. It uses the standard positive mass theorem for asymptotically flat manifolds with noncompact boundary, dimension5, including rigidity. It does not prove that theorem.

Use a flat conformal chart, followed by a local Mobius normalization, to arrange II(p)=0, g=delta locally, and tangentplane t0. Write boundary t=f3(z)+f4(z)+O(r5), z inR4, f_j homogeneous. Normalize the positive Robin Green function to leading r^-3. It exists uniquely up to this fixed normalization by coercivity of (-L,B). The boundary pole is understood as boundary-Dirac data, with BG=0 away fromp; its global positivity follows from the positive Robin Green kernel.

For a graph jet f_k, the leading boundary defect of r^-3 is
3 r^(k-5)[-(k-1)f_k+(Delta_S3 f_k+k(k+2)f_k)/8],
where f_k in the bracket denotes its restriction to S3. Thus the cubic defect is (3/8)r^-2(Delta_S3 f3-f3), and the quartic defect is (3/8)r^-1 Delta_S3 f4.

Construct q3=r^-1 Y3 on the halfspace, with
(Delta_S4-2)Y3=0, partial_out Y3=(3/8)(f3-Delta_S3 f3).
The positive operator -Delta_S4+2 with Neumann data is invertible, so this has a unique smooth angular solution. Tangential parity makes Y3 odd, hence its hemispherical mean is0. Construct q4=Y4 with
Delta_S4 Y4=0, partial_out Y4=-(3/8)Delta_S3 f4,
choosing its hemispherical mean0. Compatibility follows from integral Delta_S3 f4=0, so the Neumann problem is solvable and unique under this mean normalization.

Both q_j are harmonic and smooth up to the planar boundary away from0. Since their angular equation and boundary data are analytic, local analytic boundary regularity and harmonic continuation extend them to a fixed conic neighborhood |t|<c|z|. This extension is all that is needed on the actual graph for sufficiently smallr. Equivalently one can use reflected extensions and the thin-strip Newton estimate; no singular negative-axis point is introduced.

For G0=r^-3+q3+q4, every remaining Robin boundary error is O1. Indeed the next linear graph jet f5 gives orderr0; interactions f3 D²q3, Df3 Dq3 and H q3 also have orderr0; every other term is smaller. G0 is harmonic nearp off0. After cutting it off, coercivity solves away its smooth distant interior source and bounded local boundary residual. Standard Robin W1p regularity for every finitep makes the correction C^alpha for every alpha<1; annular estimates give the corresponding gradient remainder. Hence
G=r^-3+q3+q4+B+O(r^alpha).

Now use the complete scalar-flat/minimal-boundary metric ghat=G^(4/3)g onM\{p}. Inverted coordinates give an asymptotically flat halfspace end with decay order2>(5-2)/2=3/2. Its leading conformal perturbation fromq3 is odd of orderR^-2; the q4 perturbation is of mass orderR^-3 but has mean0. Quadratic products decay order4, beyond the mass order3. The leading graph after inversion fromf3 has height orderR^-1 and is odd, so its divergent gauge flux has zero angular mean. The critical quartic graph contributes the finite boundary-gauge mass recorded in agent3_mass_renormalization.md. Thus with the convention that the conformal B term alone has massB,
m=B-(3/8)avg_S3 f4.
This is a direct ADM bulk+edge calculation, not an identification of rawB with mass. All potential additional terms vanish either by tangential parity, by the mean-zero normalization ofq4, or by their strictly faster order.

The noncompact-boundary positive mass theorem gives m>=0. Its zero-mass rigidity gives the Euclidean halfspace; conformal compactification then makes (M,g) conformally equivalent to the hemisphere. Therefore in the problem's nonhemisphere setting m>0.

The linear spherical Pohozaev ofG has limit -(9/4)|S4| B. q3 isodd; q4 hasmean0; their quadratic terms vanish bypositivepowersr. Since |S3|/|S4|=3/4, the adapted invariant is
lim_(r->0)[P_r(G)+(9/8)integral_S3 f4]=-(9/4)|S4|m<0.
For a Green sum with positive ownpole coefficienta, scale the jet term by a²; the ownmass contribution remains strictlynegative and contributions fromotherpositivepoles are also negative. This is exactly the GM contradiction required by agent2_n5_renormalized_SP.md and agent3_compactness_bridge.md.

With those independently proved SP and bridge lemmas, this closes the dimension5 compactness subcase. It does not settle n6 or the sharp n7 existence threshold.
