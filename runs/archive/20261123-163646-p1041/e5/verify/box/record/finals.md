# agent_1: last reply

(none)

# agent_2: last reply

(none)

# agent_3: last reply

(none)

# agent_4: last reply

Proved and independently checked:

1. **Central-interval propagation.** If \(N=2^m\), then
   \[
   \mathcal W_{m+1}\supseteq \mathcal W_m+\mathcal W_m
   \]
   via \(F(x,t)=(1+t)g(x)+th(x)\). Thus the central interval at \(m=14\) propagates to every larger \(m\).

2. **Central certificate independently replayed.** `workspace/agent2_central_certificate.py` successfully verifies all even weights in \([336,16048]\) for \(\mathrm{RM}(7,14)\).

3. **Finite-dimensional exclusion reduction.** A support of size at most \(334\) has at most
   \[
   \binom{334}{2}=55611<2^{16}
   \]
   nonzero differences. Collision-free projection therefore reduces any prospective excluded low weight to ambient dimension at most \(15\), preserving the corank-seven degree bound.

4. **Autocorrelation-degree lemma.** If \(f\) has degree at most \(r\le m-2\), with support \(S\), then
   \[
   q(v)=\frac{|S\cap(S+v)|}{2}\pmod2
   \]
   is a Boolean polynomial of degree at most \(2r-m\). Writing the ANF monomial masks as \(A_i\), its exact formula is
   \[
   q(v)=
   \sum_{\substack{i<j\\A_i\cup A_j=[m]}}
       \prod_{k\in A_i\cap A_j}(1+v_k).
   \]
   The proof uses the integer ANF expansion modulo \(4\): higher cross terms cancel by correlation symmetry, and diagonal monomial correlations are divisible by \(4\).
   
   `workspace/agent4_autocorrelation.py` checks the exact identity and degree bound; 80 independent finite tests passed.

**Still unresolved:** a verified weight-\(310\) construction, and the substantive low-weight exclusions—particularly \(322,326,330,334\) in dimension \(14\), plus the constant-\(q=1\) case in dimension \(15\). None of the failed searches constitutes exclusion evidence.