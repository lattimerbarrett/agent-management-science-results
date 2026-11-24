# Verified auxiliary proof (agent_2)

Write K_A={e:e in Gamma_e(A)} and S_A=complement(K_A).
All joins use even/odd coding. Every c.e. set is enumeration reducible to every oracle, by axioms with empty use.

## Uniform complement completeness
Given an enumeration operator Gamma_i and x, let q(i,x) index the operator Lambda which outputs all natural numbers if x appears in Gamma_i(Z), and outputs nothing otherwise. This is a computable index transformation by s-m-n; its enumerated axioms simply replace every (x,F) axiom of Gamma_i by (y,F) for all y. Therefore q(i,x) in Gamma_q(i,x)(A) iff x in Gamma_i(A), so
  x not in Gamma_i(A) iff q(i,x) in S_A.
In particular the complement of any set enumeration reducible to A is many-one reducible to S_A.

K_A <=_e A directly: enumerate (e,F) whenever (e,F) occurs in W_e. Conversely, taking Gamma_i to be the identity in the preceding construction yields x in A iff q(i,x) in K_A, so A <=_m K_A.
If A <=_e B, then K_A <=_e B and therefore S_A <=_m S_B by complement completeness. Thus the skip is degree invariant.

## Cototality test
The degree of A is cototal iff A <=_e S_A.
Forward: choose B =_e A with B <=_e complement(B). Complement completeness gives complement(B) <=_m S_A, hence A <=_e S_A.
Reverse: K_A =_e A and K_A <=_e S_A = complement(K_A), so K_A is a cototal representative of the degree.
Consequently cototal A has literally self-total skip: complement(S_A)=K_A <=_e A <=_e S_A. This conclusion is stronger than merely asserting that the skip's degree is total.

## Low hierarchy exclusion
Let K be the ordinary halting set and H=K join complement(K). Then H =_e complement(K): K is c.e. and the other summand is the oracle itself. By complement completeness applied to a fixed ordinary c.e. halting set, complement(K) <=_m S_A uniformly for every A. Hence H <=_e S_A for every A.
Every Sigma^0_2 set is c.e. relative to K, hence enumeration reducible to the total oracle H. Thus if A is Sigma^0_2, then A <=_e H <=_e S_A. By the cototality test A is cototal and S_A is literally self-total. Its degree is therefore cototal: for any literally self-total X, X join complement(X) =_e X and this join is equivalent to its complement.
The hierarchy inclusions Sigma^0_1 union Pi^0_1 subset Sigma^0_2 follow by dummy quantifiers. Therefore none of (Sigma,1),(Pi,1),(Sigma,2) can be in E.

## Every Pi^0_2 degree is weakly cototal
If A is Pi^0_2, put B=A join K. Since K is c.e., B =_e A. Its complement is complement(A) join complement(K). Here complement(A) is Sigma^0_2, hence <=_e H =_e complement(K), so complement(B) =_e complement(K), a total degree.
Crucially this does not assert that complement(A) itself has total degree.

## Total skip implies weakly cototal predecessor
If the degree of S_A is total, take B=A join K_A =_e A. Then complement(B)=complement(A) join S_A =_e S_A by complement completeness. Thus B witnesses weak cototality of the degree of A.

## Relative version and closure under skip
For a literally self-total oracle T, let K^T be its ordinary Turing halting set. Then K^T <=_e T, while complement(K^T) has the total degree of T's Turing jump. If X is Pi^0_2 relative to T and T <=_e X, set Y=X join K^T =_e X. Its complement is complement(X) join complement(K^T), equivalent to complement(K^T) since complement(X) is Sigma^0_2 relative to T. Thus X is weakly cototal.
If A is weakly cototal, choose B =_e A with D=complement(B) =_e a literally self-total T. Since D is c.e. relative to T, B is co-c.e. relative to T, and S_B is Pi^0_2 relative to T. Also T <=_e D <=_e S_B by complement completeness. Applying the relative version shows that S_B, and therefore S_A, has weakly cototal degree.

## What these lemmas do NOT prove
They give only E subset ({Pi} x {m>=2}) union ({Sigma} x {m>=3}). They neither supply a Pi^0_2 noncototal-skip example nor prove universal preservation of cototality by skip on weakly cototal degrees. None of the abandoned priority or antichain proposals is used above.
