from pathlib import Path
text=r'''# A nonfaithful expectation onto a masa of the hyperfinite II1 factor

Let R be the weak closure of the infinite tensor product of M_2(C), with product normalized trace tr. Let D be its product diagonal masa. Put e_+=(1/2)[[1,1],[1,1]]. For n>=1 let q_n be e_+ on tensor coordinates n+1,...,2n and the identity elsewhere. Then q_n is a projection with tr(q_n)=2^{-n}, and its diagonal conditional expectation is E_D(q_n)=2^{-n}1. Define the normal state
    phi_n(x)=2^n tr(q_n x).
Thus phi_n restricted to D is exactly tr restricted to D.

For any d in D, approximate d in L2(tr) by diagonal finite-tensor d_k. If n>=k then q_n commutes with d_k, so phi_n([d_k,x])=0. State Cauchy-Schwarz and phi_n|D=tr|D give
    |phi_n([d,x])| <= 2 ||x|| ||d-d_k||_2.
Consequently every weak-* cluster point phi of phi_n is D-central, and phi|D=tr|D.

For x>=0, the functional d -> phi(dx) on D is positive (D-centrality gives phi(dx)=phi(d^{1/2} x d^{1/2}) for d>=0) and bounded above by ||x|| tr(d). Commutative Radon-Nikodym supplies a unique E(x) in D_+ with 0<=E(x)<=||x||1 and
    tr(d E(x))=phi(dx) for all d in D.
Linear extension defines a positive unital map E:R->D. D-centrality implies E(a x b)=a E(x)b for a,b in D, and E|D=id. Thus E is a conditional expectation. Also tr(E(x))=phi(x).

Fix N>=3 and let r=join_{n>=N}q_n in R. Normality and finite additivity of the ordinary trace give
    tr(r) <= sum_{n>=N}2^{-n}=2^{1-N}<1.
For n>=N, q_n<=r, so phi_n(r)=1. Hence phi(r)=1 and phi(p)=0 for the nonzero projection p=1-r. Positivity and faithfulness of tr on D then give E(p)=0. Thus E is not faithful.

In particular there are no nonzero e in Proj(D), delta>0 with epe>=delta e: applying E would give 0>=delta e. This disproves a proposed universal local-compression route to faithful expectations, even in a finite von Neumann factor. It does NOT disprove existence of some faithful expectation (the usual trace-preserving E_D is faithful), and it does NOT prove the main AW*-factor assertion.

Exact finite tensor checks are in agent4_nonfaithful_expectation_checks.py.
'''
Path('workspace/agent4_expectation_counterexample.md').write_text(text)
print('Saved full counterexample proof:',len(text),'characters')
