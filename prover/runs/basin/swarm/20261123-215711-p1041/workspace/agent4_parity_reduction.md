# Group-algebra parity reduction (proved)
Let G=F2^m and R=F2[G], with e_x e_y=e_(x+y), and z_i=1+e_(unit_i). Then z_i^2=0. For a support S put F=sum_(x in S)e_x. RM(m-7,m) membership is equivalent to F in I^7, where I=(z_1,...,z_m), because the coefficient of z_A is sum_(x in S)prod_(i in A)x_i and all moments of degree at most6 vanish.

For an even-cardinality support, define
q(F)=sum_{unordered distinct x,y in S}e_(x+y) + (|S|/2 mod2)e_0.
Its polarization on even vectors is q(F+H)+q(F)+q(H)=FH. For each squarefree augmentation monomial z_A with |A|>=2, q(z_A)=0, since it is the indicator of a flat of size2^|A| and every nonzero internal difference occurs 2^(|A|-1) times as an unordered pair. Hence if F=sum_A c_A z_A lies I^7, q(F)=sum_(A<B)c_A c_B z_A z_B lies I^14.

At m=15, I^14 corresponds to Boolean functions of degree<=1. If |S|=2 mod4, q(F)(0)=1, so q(F)(a)=1+l(a) for a linear form l. For a!=0, q(F)(a)=|S intersection(S+a)|/2 mod2. Therefore the quotient derivative weight d(a)=|S|-|S intersection(S+a)| obeys d(a)/2 mod2=l(a). (For a=0, d(0)=0 and this also holds.)

Suppose the weight w is absent from RM(7,14), but occurs in RM(8,15), and w<=334 is 2 mod4. If l!=0, for every a outside ker(l), the quotient derivative has weight d(a)=2 mod4 and cannot equal w. Thus d(a)<=w-4 and I(a)>=4. Writing S=S0 disjoint-union S1 by the two l-levels, sum_(l(a)=1)I(a)=2|S0||S1|. Since there are 2^14 such a, 2|S0||S1|>=2^16. But 2|S0||S1|<=w^2/2<=334^2/2<2^16, contradiction. Therefore any counterexample at m15 must satisfy l=0 and q(F)=J.

This does NOT exclude l=0. Example F=z_A+z_B for complementary A,B of sizes7,8 has support382, valuation7, q(F)=J.
