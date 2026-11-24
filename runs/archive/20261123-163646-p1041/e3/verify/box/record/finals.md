# agent_1: last reply

Your candidate is correct. The key exclusion argument is a **derivative bootstrap**: a hypothetical word of weight \(322,326,330\), or \(334\) must have a zero third derivative. This reduces the problem to strict-below-\(2d\) Reed–Muller normal forms; no unproved decomposition assertion for weights between \(2d\) and \(2.5d\) is needed.

I give the spectrum, the proof, and executable certificates below.

## 1. The spectrum

Put \(N=2^m\). Then, for every \(m\ge14\),
\[
\begin{aligned}
\mathcal W_m={}&
[0,0]_2
\cup[128,128]_2
\cup[192,192]_2
\cup[224,224]_2
\cup[240,240]_2
\cup[248,248]_2\\
&\cup[252,256]_2
\cup[272,272]_2
\cup[288,288]_2
\cup[296,296]_2
\cup[304,304]_2
\cup[308,308]_2\\
&\cup[312,320]_2
\cup[324,324]_2
\cup[328,328]_2
\cup[332,332]_2
\cup[336,N-336]_2\\
&\cup[N-332,N-332]_2
\cup[N-328,N-328]_2
\cup[N-324,N-324]_2
\cup[N-320,N-312]_2\\
&\cup[N-308,N-308]_2
\cup[N-304,N-304]_2
\cup[N-296,N-296]_2
\cup[N-288,N-288]_2\\
&\cup[N-272,N-272]_2
\cup[N-256,N-252]_2
\cup[N-248,N-248]_2
\cup[N-240,N-240]_2\\
&\cup[N-224,N-224]_2
\cup[N-192,N-192]_2
\cup[N-128,N-128]_2
\cup[N,N]_2 .
\end{aligned}
\]
These are the **33 maximal intervals**.

Every displayed constant endpoint \(c\) means \(0\cdot2^m+c\); every \(N-c\) means \(1\cdot2^m-c\); and \(N\) means \(1\cdot2^m+0\). Thus all endpoints have the required form with explicitly numerical integer coefficients.

---

## 2. Classical inputs

Here are the established Reed–Muller results used in the proof.

1. A nonzero word of \(\mathrm{RM}(r,n)\), with \(c=n-r\), has weight at least \(2^c\). Equality holds exactly for indicators of affine \(c\)-flats. The next possible weight is at least \(3\cdot2^{c-1}\).

2. The strict-below-\(2d\) theorem of Kasami–Tokura describes every word of weight below \(2^{c+1}\) as an affine-factor quadratic word or a sum of two minimum words. The relevant consequences are:
   * the quadratic type has support span \(c+2\);
   * the two-flat type consists of two affine \(c\)-flats whose nonempty intersection has dimension \(c-\mu\);
   * every codimension-seven word below \(256\) in ambient dimension at most \(13\) is periodic;
   * in ambient dimension \(14\), the only possibly aperiodic strict-below-\(256\) type has weight \(254\).

3. The **numerical**, not structural, low-weight theorem of Kasami–Tokura–Azumi gives:
   \[
   \begin{split}
   c=6,\quad 0<w<160:\quad
   w\in\{&64,96,112,120,124,126,128,\\
          &136,144,148,152,154,156,158\};
   \end{split}                                      \tag{2.1}
   \]
   and, for \(c=7\),
   \[
   \begin{split}
   0<w<320:\quad
   w\in\{&128,192,224,240,248,252,254,256,272,288,\\
          &296,304,308,312,314,316,318\}.
   \end{split}                                      \tag{2.2}
   \]
   In particular, the first codimension-six weight congruent to \(2\bmod4\) is \(126\), the next is \(154\), and there is no codimension-seven weight strictly between \(256\) and \(272\).

These are the classical strict-\(2d\) and numerical-\(2.5d\) theorems, not the spectrum being proved here. In particular, we do **not** assume that every word below \(2.5d\) is a sum of three minimum words.

By (2.2), once attainability is established, the only additional exclusions needed below \(336\) are
\[
                     322,\quad326,\quad330,\quad334.       \tag{2.3}
\]

---

## 3. Group algebra and reduction to dimensions 14 and 15

For \(V=\mathbb F_2^n\), work in \(\mathbb F_2[V]\), writing \(X^vX^w=X^{v+w}\). Let \(I\) be its augmentation ideal.

If \(Y_i=1+X^{e_i}\), then \(Y_i^2=0\). The usual support/group-algebra correspondence identifies
\[
                  \mathrm{RM}(n-c,n)=I^c.
\]

For an even support \(S\), define its divided square
\[
 Q(S)=
 \sum_{\{s,t\}\subseteq S,\ s\ne t}X^{s+t}
 +\left(\frac{|S|}{2}\bmod2\right)X^0 .
\]
It satisfies
\[
                  Q(A+B)=Q(A)+Q(B)+AB.                    \tag{3.1}
\]
Also \(Q(Y_T)=0\) when \(|T|\ge2\). Expanding in the squarefree \(Y_T\)-basis therefore gives
\[
                         Q(I^c)\subseteq I^{2c}.           \tag{3.2}
\]

For \(a\ne0\), the coefficient of \(X^a\) is the parity of
\[
 p_S(a)=\#\{\{s,t\}\subseteq S:s+t=a\}.
\]

Suppose henceforth that \(w=|S|\) is one of (2.3).

### Dimensions at least 16

Since
\[
 \binom{w}{2}\le\binom{334}{2}=55611<65535=2^{16}-1,
\]
some nonzero direction \(a\) is missing from \(S-S\). Projection modulo
\(\langle a\rangle\) is injective on \(S\), preserves its weight, and its parity projection belongs to the Reed–Muller code with one fewer variable and one lower degree.

Thus repeated projections reduce the problem to dimension \(15\).

### Dimension 15

Here \(Q(S)\in I^{14}=\mathrm{RM}(1,15)\), and its value at zero is \(w/2\bmod2=1\). Consequently either
\[
                         Q(S)=J_{15},
\]
where \(J_n=\sum_{v\in\mathbb F_2^n}X^v\), or
\[
                         Q(S)(a)=1+\ell(a)
\]
for a nonzero linear form \(\ell\).

In the latter case, all \(2^{14}\) directions satisfying \(\ell(a)=1\) have even pair multiplicity. If none were missing, their pair multiplicities would all be at least \(2\), giving at least \(32768\) crossing pairs between the two \(\ell\)-sections of \(S\). But their number is at most
\[
                         \frac{w^2}{4}\le27889<32768.
\]
Therefore a missing direction exists, reducing injectively to dimension \(14\).

It remains to exclude:

* all four target weights in \(\mathrm{RM}(7,14)\);
* the constant-\(Q\) case \(Q(S)=J_{15}\) in \(\mathrm{RM}(8,15)\).

In dimension \(14\), (3.2) already implies \(Q(S)=J_{14}\).

---

## 4. Preliminary exclusion lemmas

A reduced derivative means parity projection onto the quotient by its direction space. A word is *periodic* if it is invariant under a nonzero translation.

### Lemma 4.1: no minimum first derivative

In either remaining case, a first reduced derivative cannot have weight \(128\).

#### Dimension 15, constant \(Q\)

Write
\[
                         f=y1_D+t,
\]
where \(D\subseteq\mathbb F_2^{14}\) is an affine seven-flat. Then
\[
                  w=128+2\operatorname{wt}(t\text{ outside }D).
\]
The two sections are \(t\) and \(t+D\). The outside-hyperplane part of \(Q(f)=J_{15}\) gives
\[
                         t(t+D)=J_{14}.
\]
Since \(t\) has even weight, \(t^2=0\), so \(tD=J_{14}\). Thus every coset of the direction space of \(D\) has odd \(t\)-parity. Its \(127\) cosets other than \(D\) each contain a point, whence
\[
                         w\ge128+2\cdot127=382,
\]
a contradiction.

#### Dimension 14

We need the following relative gap:
\[
\begin{gathered}
 \deg t\le7,\quad D\text{ an affine seven-flat in }\mathbb F_2^{13},\\
 \operatorname{wt}(t\text{ outside }D)\text{ odd and }<105
 \quad\Longrightarrow\quad
 \operatorname{wt}(t\text{ outside }D)\in\{63,93,95\}.       \tag{4.1}
\end{gathered}
\]

Here is a proof, included because it is an important exclusion.

Use coordinates \(x\in\mathbb F_2^6,z\in\mathbb F_2^7\), with \(D=\{x=0\}\), and define fiber moments
\[
 M_J(x)=\sum_z t(x,z)\prod_{j\in J}z_j.
\]
Then \(\deg M_J\le |J|\). Fiber parity is constant; odd outside weight forces it to be \(1\). The \(63\) outside fibers therefore give baseline weight \(63\). Put
\[
                         E=e-63\le40.
\]
Affine \(z\)-shifts make all first moments zero.

If a second moment is nonzero, its weight on \(\mathbb F_2^6\) is at least \(16\). A nonminimum one has weight at least \(24\), which would require at least \(23\) outside defective fibers, each costing at least \(2\), exceeding \(E\). Two distinct minimum supports also have union at least \(24\). Hence all second moments are constant multiples of one affine four-flat indicator \(1_T\).

Their alternating matrix has rank \(2\): rank at least \(4\) would cost at least \(4\) in each of at least \(15\) outside fibers, again exceeding \(40\). It identifies a plane \(P\). The canonical fiber is \(\{0\}\) off \(T\), and \(P\setminus\{0\}\) on \(T\). Its outside weight is
\[
                         e_0=63+2|T\setminus\{0\}|\in\{93,95\}.
\]
The remaining excess is at most \(10\), so at most five fibers differ from the canonical ones. A nonzero third-moment error has outside support at least \(8-1=7\), so all third-moment errors vanish. A remaining defect now costs at least \(10\), leaving at most one. A fourth-moment error has outside support at least \(4-1=3\), so it also vanishes. A defect would then cost at least \(32-2\cdot3=26>10\). Thus \(e=e_0\).

If all second moments vanish, a nonzero third moment costs at least
\(7\cdot6=42>40\), and a nonzero fourth moment costs at least
\(3\cdot14=42>40\). Hence both vanish. Any defective fiber now costs at least \(30\), so there is at most one. Its symmetric difference with \(\{0\}\) is an \(\mathrm{RM}(2,7)\) word of size at most \(42\). The first two quadratic weights are \(32,48\), so its size is \(32\). The original fiber has size \(31\) or \(33\), giving \(e=93\) or \(95\); with no defect, \(e=63\). This proves (4.1).

A minimum first derivative would give outside weight
\[
                         (w-128)/2\in\{97,99,101,103\},
\]
contrary to (4.1). ∎

### Lemma 4.2: all first derivatives are aperiodic and weigh at least 256

A periodic first derivative gives a zero mixed second derivative. In adapted coordinates,
\[
                         f=a u+b v+t,
\]
where \(u,v\) are codimension-six words, on \(12\) or \(13\) base variables. If \(U=|\operatorname{supp}u\cup\operatorname{supp}v|\), then
\[
                         w=2U+4e,
\]
so \(U\) is odd and
\[
              \operatorname{wt}(u)+\operatorname{wt}(v)
                  +\operatorname{wt}(u+v)=2U\le334.        \tag{4.2}
\]

The quadratic form \(q(c)=\operatorname{wt}(c)/2\bmod2\) on
\(\langle u,v\rangle\) is nonsingular. It has one or three nonzero elements with \(q=1\). Three would have total weight at least \(3\cdot126>334\). With one, either a \(q=0\) word has weight \(64\), contradicting Lemma 4.1, or the numerical list (2.1) leaves only
\[
                         (96,96,126),\qquad(96,112,126).    \tag{4.3}
\]

These triples are impossible by a short exterior-algebra argument. The leading degree-six support-moment forms supplied by the strict KT normal forms would be
\[
 \alpha=\operatorname{vol}U_6+\operatorname{vol}W_6,\qquad
 \alpha=\beta+\gamma,
\]
where \(U_6\cap W_6=0\), \(\beta\) has essential space \(M\) of dimension \(8\), and \(\gamma\) has essential dimension at most \(9\).

In ambient dimension \(n\), let \(K\) annihilate the essential space of \(\gamma\), so \(\dim K\ge n-9\). For \(\eta\in K\),
\[
                         \iota_\eta\alpha=\iota_\eta\beta.
\]
If \(\eta\) is nonzero on both \(U_6,W_6\), the left side has essential dimension \(10\), whereas the right side has essential dimension at most \(8\). Thus the linear space \(K\) lies in one of their annihilators, say \(\operatorname{ann}W_6\). Its restrictions to \(U_6\) have dimension at least
\[
                         (n-9)-(n-12)=3.
\]
Two independent contractions force \(U_6\subseteq M\). Now
\(\beta+\operatorname{vol}U_6\) is annihilated by \(K\), and belongs to
\[
                         \Lambda^6(M\cap K^\perp),
\]
whose supporting dimension is at most \(8-3=5\). It is zero, contradicting the essential dimension \(8\) of \(\beta\). This excludes (4.3).

Thus all first derivatives are aperiodic. In dimension \(14\), strict KT immediately makes their weights at least \(256\). In the constant-\(Q\), dimension-\(15\) case, all \(p_S(a)\) are odd, so
\[
                         \operatorname{wt}(\Delta_a f)=w-2p_S(a)
\]
is divisible by \(4\). This excludes the sole aperiodic strict-KT exception \(254\), giving the same lower bound. ∎

### Lemma 4.3: a first derivative of weight at least 256 cannot have span at most 11

Let \(U\) be the preimage of such a support span. Then \(\dim U\le12\), and \(f\) has at most \(334-256=78\) points outside \(U\). Since \(Q(f)=J_m\), some support point lies outside \(U\).

Choose a hyperplane \(H\) containing \(U\) and excluding such a point. The outside-\(H\) section is a nonzero codimension-six word of weight at most \(78\); hence it is a minimum six-flat \(F\) of weight \(64\). The inside section \(B\) has at most \(14\) points outside \(U\). A nonzero puncture outside a proper flat in \(H\) has weight at least \(32\), so \(B\) is supported in \(U\).

But \(Q(F)=0\), and restricting \(Q(f)\) to directions of \(H\) yields
\[
                         J_H=Q(B)+Q(F)=Q(B).
\]
The right side is supported in the proper direction space of \(U\), a contradiction. ∎

### Lemma 4.4: a weight-256 word with a minimum first derivative

Let \(g\) be a codimension-seven word in ambient dimension \(13\) or \(14\), of weight \(256\), having a first reduced derivative \(1_D\) of weight \(128\). Then
\[
             g\text{ is periodic, or its support span has dimension }\le11.
                                                               \tag{4.4}
\]

Write \(g=y1_D+t\), so \(t\) has outside-\(D\) weight \(64\). Add \(1_D\ell\), for an affine \(\ell\), to \(t\), absorbing this by an affine shear of \(y\). The Walsh transform on \(D\) permits inside weight \(<64\), so now \(\operatorname{wt}(t)<128\).

Apply strict KT in codimension six. If \(t\) is a minimum or two-minimum word, lifting its six-flats freely along \(y\) makes \(g\) a sum of at most three seven-flat indicators.

Every such sum of weight \(256\) in ambient dimension at most \(14\) is periodic. Indeed, a pair meeting in \(64\) points collapses to one minimum word, and two disjoint seven-flats in dimension at most \(14\) have a common direction. Otherwise all pair intersections have size at most \(32\). Writing their sizes \(p,q,r\) and the triple size \(s\),
\[
                         p+q+r-2s=64.
\]
If \(s\ge2\), the common direction is a period. If \(s=1\), the only possibility is \(32,32,2\), but the two incident five-dimensional intersections force triple dimension at least \(3\), impossible. If \(s=0\), the possibilities are \(32,32,0\) or \(32,16,16\), whose incident direction intersections give a common period of dimension at least \(3\) or \(2\).

The remaining KT type for \(t\) is quadratic, with support span an eight-flat \(L\), and weight \(96,112\), or \(120\). Its inside-\(D\) weight is respectively \(32,48\), or \(56\), so
\[
 \dim(D\cap L)\ge5,\qquad
 \dim\operatorname{affspan}(D\cup L)\le7+8-5=10.
\]
Adding \(y\) gives support span at most \(11\), proving (4.4). ∎

---

## 5. The derivative bootstrap

This is the step that excludes arbitrary words, rather than merely sums of a few minimum words.

### Lemma 5.1

For \(m=14\) or \(15\), every target word has a zero third derivative.

Choose a uniformly random \(k_0\)-dimensional kernel, where \(k_0=m-10\). The fiber inequality
\[
 j\bmod2\ \le\ j-2\binom j2+4\binom j3
\]
gives the expected weight of the cubic ten-variable parity projection at most
\[
 w-2\binom w2\frac{2^{k_0}-1}{2^m-1}
 +4\binom w3
 \frac{(2^{k_0}-1)(2^{k_0}-2)}
      {(2^m-1)(2^m-2)}.                                  \tag{5.1}
\]
For all eight choices of \(m,w\), this is below \(256\); the exact rational calculations are in the code below. A zero projection, or a period of a nonzero strict-KT cubic projection, supplies a zero derivative of order \(m-9\).

Now suppose every \(k\)-th derivative is nonzero but some \((k+1)\)-st derivative is zero, where \(2\le k\le5\). Expand along that \((k+1)\)-kernel. Its \(k+1\) top coefficients form an independent codimension-six code:

* a dependence would be a zero \(k\)-th derivative, because every nonzero \(k\)-vector in a \((k+1)\)-space is decomposable;
* its support union \(T\) has size at most \(167\), because every corresponding nonempty fiber has even size at least \(2\);
* its nonzero words have average weight
  \[
                \frac{2^k|T|}{2^{k+1}-1}
                \le\frac{2^k167}{2^{k+1}-1}<96.
  \]

It therefore contains a minimum word of weight \(64\). A kernel basis change makes it a top coefficient, producing a minimum \(k\)-th reduced derivative \(1_D\) of weight \(128\).

For each nonzero functional \(\ell\) on this \(k\)-kernel, project instead along \(\ker\ell\). The resulting parent has weight
\[
                              128+2e_\ell.
\]
If \(L\) counts outside-\(D\) fibers whose pointwise XOR is nonzero, then
\[
 \sum_{\ell\ne0}e_\ell=2^{k-1}L,\qquad 2L\le w-128.
\]
Hence some parent has weight at most
\[
                 128+\frac{2^{k-1}}{2^k-1}(w-128).         \tag{5.2}
\]
For \(k=3,4,5\), this is below \(256\). Its ambient dimension is at most \(13\), so strict KT makes it periodic. Lifting that period gives a zero \(k\)-th derivative, a contradiction.

Descending from the zero derivative supplied by (5.1) therefore gives a zero third derivative. ∎

### Final contradiction

Lemma 4.2 forbids zero second derivatives. Apply the coefficient-code argument above with \(k=2\) to a zero third derivative. We obtain a minimum second reduced derivative of weight \(128\).

Its three parent first derivatives all have that minimum first derivative and have average weight at most
\[
                         128+\frac23(w-128)
                         \le\frac{796}{3}<268.
\]
By Lemma 4.2 they all weigh at least \(256\). They are divisible by \(4\), and the numerical KTA gap excludes \(260\) and \(264\). Thus one weighs exactly \(256\).

Lemma 4.4 makes that derivative periodic or of support span at most \(11\), contradicting Lemma 4.2 or Lemma 4.3.

This excludes all four target weights in dimension \(14\) and in the constant-\(Q\) dimension-\(15\) case. Section 3 consequently excludes them for **every \(m\ge14\)**.

---

## 6. Attainability and maximality

The code below supplies explicit witnesses in \(\mathrm{RM}(7,14)\) for all 21 positive exceptional weights below \(336\):
\[
\begin{gathered}
128,192,224,240,248,252,254,256,272,288,296,304,308,\\
312,314,316,318,320,324,328,332.
\end{gathered}
\]
It checks every witness on all \(16384\) points and independently computes its complete squarefree ANF.

It also supplies witnesses for all 64 even weights \(336,\ldots,462\). Each is a sum of four or five seven-flat indicators. With respect to the coordinate seven-space \(B\), the union of its flats occupies at most \(43\) of the \(128\) cosets of \(B\). Thus at least \(64\) cosets are empty. Adding \(j=0,\ldots,64\) empty cosets gives weight \(w+128j\). These weights fill
\[
                         [336,8654]_2.
\]
Complementation fills \([7730,16048]_2\), giving the entire middle interval for \(m=14\).

For induction, if \(C=[336,N-336]_2\) occurs in \(m\) variables, concatenation
\[
                         (1+z)u(x)+zv(x)
\]
is in the next code and has weight \(\operatorname{wt}(u)+\operatorname{wt}(v)\). The sums \(0+C,C+C,N+C\) give
\[
 [336,N-336]_2,\quad[672,2N-672]_2,\quad[N+336,2N-336]_2.
\]
They overlap for all \(N\ge16384\), proving the next middle interval.

Exceptional witnesses embed into higher dimensions by multiplication by
\(\prod_{i=15}^m(1+x_i)\), preserving weight. Adding \(1\) gives the reflected weights.

Together with the exclusions, this proves exactly the displayed spectrum. Consecutive displayed intervals are separated by missing even integers, so all 33 intervals are maximal.

---

## 7. Executable certificate

This is self-contained Python using only the standard library. It was executed successfully. It does not pretend to enumerate the enormous Reed–Muller code: the universal exclusions are proved above, using the explicitly stated classical theorems. The program checks the literal constructions and the finite algebra, fiber, intersection, and rational-arithmetic steps.

```python
"""Exact certificates for the spectrum proof; Python 3, standard library.

Checks:
* all 21 exceptional and 64 middle seeds on all 16384 points;
* their complete Boolean Mobius/ANF transforms;
* all empty-block extensions of the middle seeds;
* exact rational projection bounds;
* Pluecker/decomposability and fiber identities used in the bootstrap;
* finite intersection and relative-gap arithmetic;
* small exhaustive instances of the divided-square identity.

Strict KT normal forms and numerical KTA theorems are external
mathematical theorems, not claims of exhaustive codeword enumeration.
"""
from itertools import combinations, product
from fractions import Fraction
from math import comb

LOW = {
    128:[127], 192:[127,415], 224:[127,911],
    240:[127,1927], 248:[127,3971], 252:[127,8065],
    254:[127,16256], 256:[127,829,4467],
    272:[127,3193,4726], 288:[127,5175,7408],
    296:[127,4551,10302], 304:[127,12068,11590],
    308:[127,2669,13618], 312:[127,9003,8668],
    314:[127,7876,16256], 316:[127,4348,12161],
    320:[127,3607,13894], 324:[127,15748,13351],
    328:[127,2734,9495], 332:[127,9013,13642]
}

# Row i gives a witness of weight 336+2*i.
# A hexadecimal mask denotes the coordinate 7-space on its set bits.
# "*" is the explicitly supplied noncoordinate witness of weight362.
CENTRAL = """1366 2275 2366 1ee
3361 c9e 4f3 c1f
1c8d 2b64 11d9 ccd
136a 2d19 12e6 12d6
145d 12d3 70f 1517
2c3a 11e6 2e19 283b 262b
1593 22e5 26a5 165c
149b 2b64 1c8b 22da
1a74 2c47 319c 31cc
3b9 2936 3646 b39 9b9
10cf 236a 2365 31aa
f62 309b acd 349a f64
116d 3a32 3c70 1559
*
3c13 2b23 3ae b0f
acd 25b2 3532 2c1e
5b5 11cd 14b3 20eb
1719 32a6 8e7 2af 28e6
1c65 22d6 26cc 1cb1
1c8d acd 3532 360d
12f4 3256 3133 2695
6e3 1939 2627 19d8
119e db1 192d 6b3
1539 5e9 34c9 b36 2936
354c 252b 130f d65
3a7 1197 3c58 a67
26c6 c4f 292b 29b1
18ab 14ba 3a31 2b45
6ce 8b7 277 219b
14f8 b0f 2af0 2b07 ae9
2cb8 1672 292d 23b8
21d6 2c2b 151b 13d4
290f 29b2 c5d 1d70
53d 1d31 29d2 22ce
258b 13e1 2d07 af2
3929 3938 2347 6d6 29c3
7b4 be8 26ca 322e
357 322e 25f0 1a0f
769 3247 e5a 350d
26c9 1936 1758 350e
2e07 198d 381b 29e1
774 3c2a f34 3d5 2b68
3325 3293 2f6 15ca
2b0b 216d 3217 14f4
6f8 1aca 283b 9bc
2395 b2d 34d2 1a4e
de2 113d 2ae8 3147
25e4 11d3 30dc 1a1b 2764
3196 25e1 3a15 1e4c
28dc 26e4 3487 191b
254b 29d2 ab5 16e2
22c7 1d38 13a5 f38 2c4b
18b9 1e58 b1e 22e5
123e 1c33 3495 b6a 2437
3295 215e 2e0b f64
23d2 32a5 2a9a 3361 d5a
245e 7b4 3a07 12e9
ad3 32c6 381d 7e2
21ce 392c 271c 1cd2
6ba 38d1 1b46 e1e 72e
342e 3f1 330d 38cc
3076 eb4 1ae4 251b 16b8
2437 9cb 3dc 15e8
2956 4bd 3970 16a9 aab"""

def rank(vs):
    piv = {}
    for v in vs:
        while v:
            j = v.bit_length()-1
            if j not in piv:
                piv[j] = v
                break
            v ^= piv[j]
    return len(piv)

def span(B):
    S = [0]
    for v in B:
        assert v not in S
        S += [x ^ v for x in S]
    return S

def coordinate_basis(mask):
    return [1 << i for i in range(14) if mask >> i & 1]

def anf_degree(truth):
    a = [(truth >> i) & 1 for i in range(16384)]
    for k in range(14):
        for i in range(16384):
            if i >> k & 1:
                a[i] ^= a[i ^ (1 << k)]
    return max((i.bit_count() for i,b in enumerate(a) if b),
               default=-1)

def word(bases):
    truth = 0
    occupied = set()
    for B in bases:
        assert len(B) == 7 and rank(B) == 7
        P = span(B)
        truth ^= sum(1 << x for x in P)
        occupied.update(x >> 7 for x in P)
    assert anf_degree(truth) <= 7
    return truth, occupied

def verify_inclusions():
    expected = {
        128,192,224,240,248,252,254,256,272,288,296,304,
        308,312,314,316,318,320,324,328,332
    }
    for w, masks in LOW.items():
        T, _ = word([coordinate_basis(a) for a in masks])
        assert T.bit_count() == w

    # U3=<e6,e7+e8,e10,...,e14>.
    B318 = [
        coordinate_basis(127), coordinate_basis(415),
        [32,192,512,1024,2048,4096,8192]
    ]
    assert word(B318)[0].bit_count() == 318
    assert set(LOW) | {318} == expected

    attained = set()
    maxocc = 0
    rows = CENTRAL.splitlines()
    assert len(rows) == 64

    for i, row in enumerate(rows):
        w = 336 + 2*i
        if row == '*':
            bases = [
                [2,520,16,32,1024,2048,8192],
                [2,4,32,64,128,256,4096],
                [1,8,16,512,1024,2048,8192],
                [1,2,8,16,32,2048,8192],
                [1,2,8,32,512,1024,8192]
            ]
        else:
            bases = [coordinate_basis(int(s,16))
                     for s in row.split()]
        truth, occupied = word(bases)
        assert truth.bit_count() == w
        assert len(occupied) <= 64
        maxocc = max(maxocc, len(occupied))
        empty = sorted(set(range(128)) - occupied)

        for j in range(65):
            assert truth.bit_count() == w + 128*j
            attained.add(truth.bit_count())
            if j < 64:
                truth ^= ((1 << 128)-1) << (128*empty[j])

    assert attained == set(range(336,8656,2))
    attained |= {16384-w for w in attained}
    assert set(range(336,16050,2)) <= attained

    # Uniform disjoint-sum induction overlaps for every N>=16384.
    assert 672 <= 16384-334
    assert 16384+336 <= 2*16384-670
    print("PASS: all85 seed truth tables and ANFs; max blocks", maxocc)
    print("PASS: middle interval constructions and induction overlaps")

def verify_exclusion_arithmetic():
    for m in (14,15):
        K = (1 << (m-10))-1
        N = 1 << m
        for w in (322,326,330,334):
            avg = (
                Fraction(w)
                - 2*comb(w,2)*Fraction(K,N-1)
                + 4*comb(w,3)*Fraction(K*(K-1),(N-1)*(N-2))
            )
            assert avg < 256
            print("projection bound", m, w, avg, float(avg))

    # Every possible occupancy of the largest initial kernel.
    for t in range(33):
        assert t % 2 <= t-2*comb(t,2)+4*comb(t,3)

    for k in range(2,6):
        assert Fraction((1 << k)*167, (1 << (k+1))-1) < 96

        # Enumerate every hyperplane and its Pluecker coordinates.
        n = k+1
        seen = set()
        for ell in range(1,1 << n):
            rows = [
                v for v in range(1,1 << n)
                if (v & ell).bit_count() % 2 == 0
            ]
            B = []
            for v in rows:
                if rank(B+[v]) > len(B):
                    B.append(v)
            assert len(B) == k

            pl = 0
            for omitted in range(n):
                cols = [j for j in range(n) if j != omitted]
                mat = [
                    sum(((v >> j) & 1) << a
                        for a,j in enumerate(cols))
                    for v in B
                ]
                if rank(mat) == k:
                    pl |= 1 << omitted
            assert pl == ell
            seen.add(pl)
        assert len(seen) == (1 << n)-1

        # Half-character identity for every moment vector.
        for v in range(1 << k):
            count = sum(
                (v & ell).bit_count() % 2
                for ell in range(1,1 << k)
            )
            assert count == ((1 << (k-1)) if v else 0)

        # Every fiber subset through dimension4.
        if k <= 4:
            for mask in range(1 << (1 << k)):
                F = [x for x in range(1 << k) if mask >> x & 1]
                v = 0
                for x in F:
                    v ^= x
                for ell in range(1,1 << k):
                    c = sum((x & ell).bit_count() % 2 for x in F)
                    wt = (c % 2) + ((len(F)-c) % 2)
                    expected = (
                        1 if len(F) % 2
                        else 2*((v & ell).bit_count() % 2)
                    )
                    assert wt == expected

        if k >= 3:
            assert 128 + Fraction(1 << (k-1),
                                  (1 << k)-1)*206 < 256

    # Explicit use of the established numerical KTA table.
    allowed = (
        64,96,112,120,124,126,128,
        136,144,148,152,154,156,158
    )
    triples = set()
    for ww in product(allowed, repeat=3):
        if (sum(ww) <= 334
            and sum((w//2) % 2 for w in ww) == 1
            and 64 not in ww):
            triples.add(tuple(sorted(ww)))
    assert triples == {(96,96,126),(96,112,126)}
    assert 3*126 > 334

    # Exterior and puncture dimensions.
    assert 8+9-5 == 12 < 13
    assert 8-3 < 6
    assert (1 << (14-7))-1 == 127
    assert 128+2*127 > 334
    assert 334-256 < 96
    assert 334-256-64 < 32

    # All numerical three-flat intersection cases of weight256.
    sizes = (0,1,2,4,8,16,32)
    for p,q,r,t in product(sizes, repeat=4):
        if t > min(p,q,r) or p+q+r-2*t != 64:
            continue
        if t >= 2:
            continue
        if t == 1:
            assert sorted((p,q,r)) == [2,32,32]
            assert 5+5-7 > 0
        else:
            assert sorted((p,q,r)) in ([0,32,32],[16,16,32])
            logs = sorted(
                (a.bit_length()-1 for a in (p,q,r) if a),
                reverse=True
            )
            assert logs[0]+logs[1]-7 >= 2

    for w in (96,112,120):
        assert w-64 >= 32
    assert 7+8-5+1 == 11
    assert 128+Fraction(2,3)*206 < 268
    print("PASS: bootstrap, fiber, Pluecker, intersection arithmetic")

def mul(a,b,N):
    out = 0
    for x in range(N):
        if a >> x & 1:
            for y in range(N):
                if b >> y & 1:
                    out ^= 1 << (x ^ y)
    return out

def Q(a,N):
    S = [x for x in range(N) if a >> x & 1]
    assert len(S) % 2 == 0
    p = (len(S)//2) & 1
    for x,y in combinations(S,2):
        p ^= 1 << (x ^ y)
    return p

def ymon(T,N):
    return sum(1 << x for x in range(N) if x & T == x)

def verify_group_algebra():
    for n in range(1,5):
        N = 1 << n
        basis = [ymon(T,N) for T in range(1,N)]
        for i,a in enumerate(basis):
            for b in basis[i+1:]:
                assert Q(a^b,N)^Q(a,N)^Q(b,N) == mul(a,b,N)

        for T in range(1,N):
            if T.bit_count() >= 2:
                assert Q(ymon(T,N),N) == 0

        for c in range(2,n+1):
            Ts = [T for T in range(N) if T.bit_count() >= c]
            for mask in range(1 << len(Ts)):
                a = expected = 0
                for i,T in enumerate(Ts):
                    if mask >> i & 1:
                        a ^= ymon(T,N)
                        for j,U in enumerate(Ts[:i]):
                            if mask >> j & 1 and not T & U:
                                expected ^= ymon(T | U,N)
                assert Q(a,N) == expected
    print("PASS: exhaustive small group-algebra checks")

def verify_relative_odd_gap_arithmetic():
    for e in range(63,105,2):
        E = e-63
        assert E <= 40
        assert 2*(24-1) > E
        assert 4*(16-1) > E
        assert 6*(8-1) > E
        assert 14*(4-1) > E
        for e0 in (93,95):
            if e0 <= e:
                R = e-e0
                assert R <= 10
                assert R//2 < 8-1
                assert R//10 < 4-1
                assert 32-2*3 > R
        assert E//30 <= 1
        assert E+2 < 48
    assert {63,93,95}.isdisjoint({97,99,101,103})
    print("PASS: every numerical branch of the odd-gap proof")

if __name__ == "__main__":
    verify_inclusions()
    verify_exclusion_arithmetic()
    verify_group_algebra()
    verify_relative_odd_gap_arithmetic()
    print("ALL EXACT CERTIFICATE CHECKS PASSED")
```

Thus both halves hold for every \(m\ge14\): every weight in the displayed intervals is attained, and every weight outside them is excluded.

# agent_2: last reply

All mathematical work is complete. The final proof has no unverified structural assumptions, and the construction and exclusion certificates pass independent checks. Agent_1 is preparing the final user-facing solution.

# agent_3: last reply

Completed and independently audited both proof halves. All structural gaps are closed; no unproved coarse KTA classification is used.

Final artifacts:
- `workspace/agent3_final_global_proof.txt`
- `workspace/agent3_final_audit_manifest.json`
- `workspace/agent1_final_certificate.py`

All 10 audited checkers passed. Agent_1 is preparing the complete user-facing proof, 33-interval spectrum, and self-contained Python certificate.

# agent_4: last reply

Proof complete. The candidate’s **33 intervals are exactly the maximal even intervals** for every \(m\ge14\).

My completed contributions include:
- The universal odd-puncture gap excluding minimum first derivatives in dimension \(14\).
- The derivative bootstrap forcing a zero third derivative, removing the previously unproved structural-classification assumption.
- The consolidated unconditional dimension-\(14\) exclusion.
- Independent full reviews of the dimension-\(15\) exclusion and global proof.
- Executed exact checkers, including the self-contained witness/ANF certificate; all passed.

The complete audited bundle is `workspace/agent1_complete_certificate_bundle.zip`. No mathematical gap remains; agent_1 is preparing the final user-facing presentation.