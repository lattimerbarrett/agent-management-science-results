# Exact all-blue-loop weighted book inequality

Let P be a finite symmetric matrix in [0,1] with diagonal zero, and let
w_j>0 sum to 1. Put f_i(j)=p_ij and use the weighted L2 inner product.
Suppose ||1-f_i||^2 <= b for every i, and <f_i,f_j> <= a whenever p_ij>0.
Assume 0<=a<=1/4. Then

b >= min(1/2, 1+2a-4 sqrt(a/3), (1-sqrt(a))^2).

Proof. It suffices b<1/2. Let S be an inclusion-maximal clique in the
support graph p_ij>0 and k=|S|. Every column has at most k-1 nonzero
entries among the rows in S: otherwise that column would extend S;
for columns in S use the zero diagonal. Write c=1-b>1/2,
F=sum_{i in S} f_i, D=<F,1>, Q=sum_{i in S} ||f_i||^2.
The row hypotheses give Q<=2D-kc. Pointwise Cauchy gives
F^2 <=(k-1) sum_{i in S} f_i^2, whence D^2<=(k-1)Q.
For k=1 this is already impossible, and for k=2 it implies
D^2-2D+2c<=0, impossible for c>1/2. Thus k>=3.

Set L=(k-1)-sqrt((k-1)^2-k(k-1)c). The preceding inequality ensures
that the radical is real and D>=L. Moreover L>1: the smaller root is
at least its value at c=1/2, which is >=1 because
(k-2)^2-(k-1)(k-2)/2=(k-2)(k-3)/2>=0.
Summing ordered red-pair inequalities gives
||F||^2-Q<=k(k-1)a. Consequently
k(k-1)a>=D^2-Q>=D^2-2D+kc>=L^2-2L+kc,
using monotonicity of D^2-2D on D>=1. The equation defining L yields
kc=2L-L^2/(k-1). Hence a>=(k-2)L^2/[k(k-1)^2].

Put p=L/(k-1). We have c=(k-1)(2p-p^2)/k and
p<=sqrt(ka/(k-2))<1 (a<=1/4, k>=3).
Since 2p-p^2 is increasing for p<=1, this gives
b>=b_k(a):=1-2(k-1)sqrt(a)/sqrt(k(k-2))+(k-1)a/(k-2).
Now let t=1/(k-2) and z=sqrt(a). The last expression is
h(t)=1-2z(1+t)/sqrt(1+2t)+z^2(1+t).
Its second derivative on [0,1] is
-2z(1-t)/(1+2t)^(5/2)<=0. Concavity implies
h(t)>=min(h(0),h(1))=min((1-z)^2,1+2z^2-4z/sqrt(3)),
as desired. QED.

This proves only the all-blue-diagonal case of the needed upper theorem.
It does NOT justify assuming that every diagonal/within-cluster color
is blue in an arbitrary graph coloring. Mixed loop colors remain a gap.
