# Uniform homology reduction (agent 3)

Work in the column-squarefree superalgebra B: x_j odd exterior generators, y_rj even commuting generators, all products of two generators in the same column zero. Differential d(y_rj)=x_j,d(x_j)=0, with odd Leibniz rule (x odd,y even). Restrict to monomials with at most b_r y's of row r; this is a subcomplex, not an algebra quotient. Set x=sum x_j. Fixed total-degree q quotient D_m^q(b)=B_{m,q}(b)/(x B_{m,q-1}(b)) has chain degree a=number y's. Original row4 spectral complex is D_m^4(2,2,2) (up to harmless orientation twists). For fixed colored set A, coefficient is Lambda^{4-a}(Z^{remaining}/Z(sum e_j)), exactly the Hodge dual row4 skeleton homology. More precisely, with U the remaining columns, Lambda^{m-5}Aug(Z^U) = Lambda^{4-a}(Aug(Z^U)^*) tensor det Aug(Z^U); and Aug(Z^U)^* = Z^U/Z(sum e_j). The colored-face orientation det Z^A combines with det Aug(Z^U) to the fixed det Z^[m]. Exterior complementation against e_1 wedge ... wedge e_m then turns deletion of a colored vertex into d(y_rj)=x_j, with y even and x odd. This explicitly accounts for the signs, rather than assuming an unproved twist.

Anchor column h gives SES
0 -> B_{m-1,q}(b) -> D_m^q(b) -> directsum_r D_{m-1}^{q-1}(b-e_r)[1] ->0.
In each colored-A component, if h unused among y's, eliminate x_h=-sum_{j!=h}x_j, yielding first piece. If y_rh present, remaining coefficient is quotient by sum of remaining x's, giving quotient. The differential of y_rh creates the connecting map +/- multiplication by x=sum_{j!=h}x_j.

Finite B data (each column-support of size q gives augmented chain complex of A_q(b), with chain degree a=#vertices):
q4,b222: H3=Z,H4=Z^2.
q3,b122: only H3=Z^2.
q2,b022: only H2=Z; b112: only H2=Z^2.
q1,b012: only H1=Z; b111: only H1=Z^2.
All are actual finite matrices checked by integer unit pivots (agent2). D^1 with either q1 capacity has H0=0 because e_j span Z^m/Z(sum e_j). Hence induction using SES gives H2(D^3(122))=0. For n=m-1,
H3(D_m^4)=M4[n]/I, M4[n]=directsum_{S subset[n],|S|4}Z g_S,
I=connecting image of three H3(D_n^3(122)).

Projection to local generator: On monomial x_j*y_A with |A|3 and total support S size4, phi=cyclicsign(double-row,single-row) if row-count type21, and zero if rainbow. cyclicsign(1,2)=cyclicsign(2,3)=cyclicsign(3,1)=+1, opposite=-1. In ordinary simplicial orientation include (-1)^{position of missing column}. phi kills boundaries and phi/6 is primitive integral on cycles (finite A4 check). Choose g_S with phi(g_S)=6; its class invariant under column permutations in B convention.

Auxiliary cycle z, deficient row1: write its integer coefficient on a colored triple as z_C. Condition dz=0 modulo x says for each valid colored pair A, sum_{allowed row c} z_{A+(c,j)}=w_A independent of j outside A. Define f(T)=Z223-Z221+Z331-Z332, where Zabc(T) sums z over colorings of T with indicated color multiset. Then
f(T)=sum_{P subset T,|P|2}h(P),
h(P)=w22(P)-w33(P)+w13(P)-w12(P),
where mixed w13,w12 sum both column assignments. Indeed W22=Z221+Z223; W33=Z331+Z332; W13=2Z331+Z123; W12=2Z221+Z123. Thus connecting coordinate
(delta z)_S=(1/6)sum_{T subset S,|T|3}f(T)=(1/3)sum_{P subset S,|P|2}h(P).
Therefore rank I <= C(n,2).

Let h_r=sum_j y_rj and E_r=sum_{i<j}y_ri*y_rj; d h_r=x,d E_r=x h_r.
For any a, z_a=(y_1a-y_2a)*E_3 is a valid auxiliary cycle: d z_a=x*(y_1a-y_2a)h_3 (up to odd reordering sign). For each T containing a, f(T)=2; otherwise0. Therefore delta z_a=r_a=sum_{S contains a}g_S.
For a!=b, z_ab=(y_1a-y_2a)*(y_2b-y_3b)*h_3 is valid (row1<=1,row2<=2,row3<=2), with dz_ab=x*(y_1a-y_2a)*(y_2b-y_3b). For each T containing a,b, f(T)=-3; otherwise0. Therefore delta z_ab=-r_ab=-sum_{S contains a,b}g_S.
Hence L=<r_a,r_ab> subset I, and rankL=C(n,2), so rankI=C(n,2).

Incidence/Bier lemma (agent4) gives M4/L=Z^{C(n,4)-C(n,2)} + Z/2; its torsion generator is w_n=sum_S g_S, and 2w_n in L. Thus M4/I is either this same group or its torsionfree quotient (any further rankzero subgroup of M4/L lies in unique Z2).
Torsion survives by direct parity, requiring no base homology calculation. Fix six labels J. For every actual relation v=delta(z), sum_{S subset J,|S|4} v_S = (1/3)*6*sum_{P subset J,|P|2}h(P) = 2*sum_P h(P), which is even. Therefore q_J(v)=sum_{S subset J}v_S mod2 annihilates I. Yet q_J(w_n)=C(6,4)=15=1 mod2. Consequently w_n survives for everym, so no further quotient. (Column deletion to D7 and the independently verified Smith computation provide an optional computational cross-check.) Final
H3(D_m)=Z^{C(n,4)-C(n,2)}+Z2=Z^{C(m,4)-C(m,3)}+Z2.

The same anchor recursion proves all low exactness directly: each auxiliary D^3(122) is exact below3, because B3(122), B2(022/112), B1(012/111) have only top homology, and D^1 has H0=0. Since B4(222) has only H3,H4, the SES shows D4 exact below3. Top H4 is free as a subgroup of free D4, and Euler characteristic gives the required polynomial.
