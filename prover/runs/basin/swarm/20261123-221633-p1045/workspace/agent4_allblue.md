# All-blue-loop graphon lemma (agent 4)
Let W be symmetric measurable [0,1]^2 ->[0,1]. Write C_R(x,y)=int W(x,z)W(y,z)dz. Assume 0<a<=b, C_R<=a for almost all pairs on which W>0 and int(1-W(x,z))^2 dz<=b for almost every x. Suppose b<1/2 and sqrt(a)+sqrt(b)<1. Then

    b >= 1+2a-4sqrt(a/3).

(The assumptions force 1/12<a<1/4.)

Proof.
1. The red support S=1_{W>0} contains a triangle. Otherwise Mantel gives int S<=1/2, and if p=int W,Q=int W^2 then Q>=2p^2, so b>=1-2p+Q>=1/2.
2. For any red-support triangle x1,x2,x3, let fi(z)=W(xi,z). Almost every such triangle has all three individual blue norms<=b and all three pair inner products<=a. The identity

    sum_i (1-fi)^2+2 sum_{i<j}fi fj = 2+(sum_i fi-1)^2

integrates to 3b+6a>=2. Therefore a>1/12.
3. The red support has no K4. Otherwise choose a good K4 with row functions fi. For 0<=lambda<=2 and s=3lambda/2, the identity

sum_i(1-fi)^2+lambda sum_{i<j}fi fj
= 4s/(1+s)+(1-lambda/2)sum_i(fi-mean(f))^2+(1+s)/4(sum_i fi-4/(1+s))^2

implies b+sa>=s/(1+s). Take s=1/sqrt(a)-1, which lies [0,3] because a>1/12>1/16 and a<1. This gives b>=(1-sqrt(a))^2, contradicting sqrt(a)+sqrt(b)<1.
4. For almost every red-support triangle, K4-freeness means that at almost every z at least one of its three fi(z) vanishes. For arbitrary x,y and lambda in [0,2], the exact identity

(1-x)^2+(1-y)^2+1+lambda*x*y
=1+2lambda/(2+lambda)+(2+lambda)/4*(x+y-4/(2+lambda))^2+(2-lambda)/4*(x-y)^2

gives, after integration, b+lambda*a >= (2+3lambda)/(3(2+lambda)). The choice lambda=2/sqrt(3a)-2 lies [0,2] because a>1/12 and a<1/4<1/3, and gives the claimed bound.

All identities are checked in agent4_cert.py. All almost-everywhere clique choices are legitimate by Fubini: the integral of the product of the support edges is positive, and the exceptional bad rows and pairs have measure zero. K4-free means t(K4,S)=0, hence for almost every support triangle the extension set has measure zero.

WARNING: This lemma does not directly apply to a mixed row-type graphon. Such mixed graphons can lie strictly above the homogeneous/random curve; purification only at an optimum remains necessary.
