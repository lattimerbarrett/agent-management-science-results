# The individual baseline: sweep solo-v1

8 lone agents a problem (no Slack, no partners, no shared workspace; otherwise a swarm's rules), not told the answer, $50 each. Solved: the verifier found a sound proof of a definite answer with no gap the agent acknowledged (stop), and the answer is right.

| problem | runs ended | solved | right answer | stops on a wrong answer | cost |
|---|---|---|---|---|---|
| p1 | 8 of 8 | 0 | 0 | 0 | $13.76 |
| p9 | 8 of 8 | 0 | 0 | 0 | $0.80 |
| p12 | 8 of 8 | 0 | 0 | 0 | $2.43 |
| p25 | 8 of 8 | 8 | 8 | 0 | $4.63 |
| p30 | 8 of 8 | 7 | 7 | 0 | $4.03 |
| p37 | 8 of 8 | 6 | 6 | 1 | $8.68 |
| p41 | 8 of 8 | 0 | 0 | 0 | $6.44 |
| p43 | 8 of 8 | 0 | 0 | 2 | $4.22 |
| p48 | 8 of 8 | 1 | 1 | 0 | $7.17 |
| all | 72 of 72 | 22 | 22 | 3 | $52.15 |

| problem | run | ended | cost | min | nudges | the agent's answer | right | verifier | solved |
|---|---|---|---|---|---|---|---|---|---|
| p1 #1 | 20261120-114859-p1 | all agents idle, the nudges used up | $1.47 | 50 | 2 | `The requested value is greater than 1 if finite; its exact value remains undetermined here.` | no | not definite | no |
| p1 #2 | 20261120-115700-p1 | all agents idle, the nudges used up | $1.67 | 50 | 2 | none | no | no answer | no |
| p1 #3 | 20261120-122041-p1 | all agents idle, the nudges used up | $2.36 | 56 | 2 | `The minimum is unresolved; if finite, it is at least 2.` | no | not definite | no |
| p1 #4 | 20261120-130124-p1 | all agents idle, the nudges used up | $1.68 | 42 | 2 | `The minimum is at least 2, but its value is undetermined.` | no | not definite | no |
| p1 #5 | 20261120-132706-p1 | all agents idle, the nudges used up | $2.04 | 56 | 2 | none | no | no answer | no |
| p1 #6 | 20261120-135808-p1 | all agents idle, the nudges used up | $1.40 | 39 | 2 | `The minimum remains unresolved; any such s must be at least 2.` | no | not definite | no |
| p1 #7 | 20261120-142330-p1 | all agents idle, the nudges used up | $1.89 | 49 | 2 | `The minimum is at least 2; its actual value remains unresolved.` | no | not definite | no |
| p1 #8 | 20261120-145032-p1 | all agents idle, the nudges used up | $1.24 | 39 | 2 | `The smallest s is unresolved; any such s must satisfy s ≥ 2.` | no | not definite | no |
| p9 #1 | 20261120-114859-p9 | all agents idle, the nudges used up | $0.10 | 5 | 2 | `\(\beta(p)\ge\max\{1,1/(p-1)\}\); the exact value is not established.` | no | not definite | no |
| p9 #2 | 20261120-115800-p9 | all agents idle, the nudges used up | $0.10 | 5 | 2 | `The exact value of β(p) is not determined; β(p) ≥ max{1, 1/(p−1)}.` | no | not definite | no |
| p9 #3 | 20261120-122542-p9 | all agents idle, the nudges used up | $0.06 | 5 | 2 | none | no | no answer | no |
| p9 #4 | 20261120-130304-p9 | all agents idle, the nudges used up | $0.08 | 5 | 2 | `The exact formula remains unresolved in my answer; I proved only β(p) ≥ max{1, 1/(p−1)}.` | no | not definite | no |
| p9 #5 | 20261120-132826-p9 | all agents idle, the nudges used up | $0.11 | 6 | 2 | `\max\left\{1,\frac{1}{p-1}\right\}\le \beta(p)\le 1+\frac{1}{p(p-1)}; the exact value is not determined.` | no | not definite | no |
| p9 #6 | 20261120-140248-p9 | all agents idle, the nudges used up | $0.17 | 7 | 2 | `\(\beta(p)\geq\max\{1,1/(p-1)\}\). The exact value is not determined in this answer.` | no | not definite | no |
| p9 #7 | 20261120-143130-p9 | all agents idle, the nudges used up | $0.11 | 6 | 2 | `\(\beta(p)\geq\max\{1,1/(p-1)\}\); no exact formula is established in the answer.` | no | not definite | no |
| p9 #8 | 20261120-145252-p9 | all agents idle, the nudges used up | $0.10 | 5 | 2 | `\(\beta(p)\ge \max\{1,1/(p-1)\}\). The exact formula is not determined.` | no | not definite | no |
| p12 #1 | 20261120-114859-p12 | all agents idle, the nudges used up | $0.23 | 9 | 2 | `43 ≤ dim_Q R^{12}(M_{25}) ≤ 44.` | no | not definite | no |
| p12 #2 | 20261120-120220-p12 | all agents idle, the nudges used up | $0.29 | 11 | 2 | `43 ≤ dim_Q R^{12}(𝓜_{25}) ≤ 44` | no | not definite | no |
| p12 #3 | 20261120-123042-p12 | all agents idle, the nudges used up | $0.76 | 22 | 2 | `43 ≤ dim_Q R^{12}(M_{25}) ≤ 44.` | no | not definite | no |
| p12 #4 | 20261120-130804-p12 | all agents idle, the nudges used up | $0.21 | 11 | 2 | `43 ≤ dim_Q R^12(M_25) ≤ 44; the exact value is not determined.` | no | not definite | no |
| p12 #5 | 20261120-133026-p12 | all agents idle, the nudges used up | $0.17 | 8 | 2 | `43 ≤ dim_Q R^{12}(M_{25}) ≤ 44.` | no | not definite | no |
| p12 #6 | 20261120-140828-p12 | all agents idle, the nudges used up | $0.17 | 8 | 2 | `43 ≤ dim_Q R^{12}(M_{25}) ≤ 44.` | no | not definite | no |
| p12 #7 | 20261120-143711-p12 | all agents idle, the nudges used up | $0.22 | 13 | 2 | `43 ≤ dim_Q R^{12}(M_{25}) ≤ 44.` | no | not definite | no |
| p12 #8 | 20261120-145332-p12 | all agents idle, the nudges used up | $0.37 | 16 | 2 | `43 ≤ dim_Q R^{12}(M_{25}) ≤ 44; the exact value remains unresolved.` | no | not definite | no |
| p25 #1 | 20261120-114859-p25 | all agents idle, the judge found the proof complete | $0.64 | 18 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p25 #2 | 20261120-120320-p25 | all agents idle, the judge found the proof complete | $0.64 | 17 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p25 #3 | 20261120-123822-p25 | all agents idle, the judge found the proof complete | $0.92 | 25 | 1 | `1/9` | yes | sound | yes |
| p25 #4 | 20261120-131144-p25 | all agents idle, the judge found the proof complete | $0.64 | 18 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p25 #5 | 20261120-133346-p25 | all agents idle, the judge found the proof complete | $0.36 | 11 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p25 #6 | 20261120-141009-p25 | all agents idle, the judge found the proof complete | $0.43 | 12 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p25 #7 | 20261120-143711-p25 | all agents idle, the judge found the proof complete | $0.54 | 16 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p25 #8 | 20261120-145832-p25 | all agents idle, the judge found the proof complete | $0.47 | 14 | 0 | `\frac{1}{9}` | yes | sound | yes |
| p30 #1 | 20261120-114859-p30 | all agents idle, the judge found the proof complete | $0.49 | 14 | 0 | `\(D_s=3\cdot 2^{s-1}-2\) for every integer \(s\ge 3\).` | yes | sound | yes |
| p30 #2 | 20261120-120320-p30 | all agents idle, the judge found the proof complete | $0.28 | 8 | 0 | `D_s = 3\cdot 2^{s-1}-2 for every integer s\ge 3.` | yes | sound | yes |
| p30 #3 | 20261120-123902-p30 | all agents idle, the judge found the proof complete | $0.41 | 12 | 0 | `\(D_s=3\cdot 2^{s-1}-2\) for every integer \(s\ge 3\).` | yes | sound | yes |
| p30 #4 | 20261120-131625-p30 | all agents idle, the judge found the proof complete | $0.38 | 12 | 0 | `\(D_s=3\cdot 2^{s-1}-2\) for every integer \(s\ge 3\).` | yes | sound | yes |
| p30 #5 | 20261120-133446-p30 | all agents idle, the nudges used up | $1.55 | 56 | 2 | `D_3=10. For s≥4, 3·2^{s-1}−3 ≤ D_s ≤ 3·2^{s-1}−2; the exact value is not established in this solution.` | no | not definite | no |
| p30 #6 | 20261120-141349-p30 | all agents idle, the judge found the proof complete | $0.26 | 7 | 0 | `\(D_s=3\cdot 2^{s-1}-2\) for every integer \(s\ge 3\).` | yes | sound | yes |
| p30 #7 | 20261120-144011-p30 | all agents idle, the judge found the proof complete | $0.31 | 10 | 0 | `D_s=3\cdot 2^{s-1}-2\quad\text{for every integer }s\ge 3.` | yes | sound | yes |
| p30 #8 | 20261120-150753-p30 | all agents idle, the judge found the proof complete | $0.35 | 13 | 0 | `D_s = 3\cdot 2^{s-1}-2 for every integer s\ge 3.` | yes | sound | yes |
| p37 #1 | 20261120-114859-p37 | all agents idle, the judge found the proof complete | $1.70 | 67 | 1 | `F(d)=d-3 for every integer d≥8.` | yes | sound | yes |
| p37 #2 | 20261120-120720-p37 | all agents idle, the judge found the proof complete | $1.30 | 54 | 1 | `F(d)=d-3 for every integer d≥8.` | yes | sound | yes |
| p37 #3 | 20261120-124723-p37 | all agents idle, the judge found the proof complete | $0.81 | 32 | 0 | `F(d)=d-3 for every integer d≥8.` | yes | sound | yes |
| p37 #4 | 20261120-131845-p37 | all agents idle, the judge found the proof complete | $1.26 | 39 | 1 | `F(d)=d-3 for every integer d≥8.` | yes | sound | yes |
| p37 #5 | 20261120-133827-p37 | all agents idle, the judge found the proof complete | $0.84 | 37 | 0 | `F(d)=d-3 for every integer d≥8.` | yes | sound | yes |
| p37 #6 | 20261120-141549-p37 | all agents idle, the judge found the proof complete | $0.72 | 35 | 0 | `F(d)=d-2 for every integer d≥8.` | no | gap | no |
| p37 #7 | 20261120-144111-p37 | all agents idle, the judge found the proof complete | $1.36 | 49 | 1 | `F(d)=d-3 for every integer d≥8.` | yes | sound | yes |
| p37 #8 | 20261120-150953-p37 | all agents idle, the judge found the proof complete | $0.68 | 41 | 0 | `For every integer d≥8, put n=λ(d−1)+1 and N=n+binom(n,2). Let X consist of the singletons and pairs of [n], let I={(v,e):v∈[n], e∈binom([n],2), v∈e}, J={(v,e):v∈[n], e∈binom([n],2), v∉e}, and ℛ=(I×[3])⊔J. Let 𝒞 be the set of distinct sets C(a,ℓ)={(v,e,i)∈I×[3]:a(v)=a(e), ℓ(v)=i}∪{(v,e)∈J:a(v)>a(e)}, as a:X→{0,…,N−1} and ℓ:X→[3] range over functions satisfying a(v)≤a(e) and a(v)=a(e)⇒ℓ(v)=ℓ(e) for every (v,e)∈I. For T⊆ℛ, put b_T=\|{C∈𝒞:C∩T=∅}\|. Then F(d)=∑_{r=3}^{n+1}⌊1/(1+∑_{T⊆ℛ}(−1)^{\|T\|}b_T^r)⌋.` | no | sound | false stop |
| p41 #1 | 20261120-114859-p41 | all agents idle, the nudges used up | $0.17 | 8 | 2 | none | no | no answer | no |
| p41 #2 | 20261120-121201-p41 | all agents idle, the nudges used up | $1.05 | 66 | 2 | none | no | no answer | no |
| p41 #3 | 20261120-125043-p41 | all agents idle, the nudges used up | $0.61 | 21 | 2 | none | no | no answer | no |
| p41 #4 | 20261120-131905-p41 | all agents idle, the nudges used up | $0.13 | 7 | 2 | none | no | no answer | no |
| p41 #5 | 20261120-134307-p41 | all agents idle, the nudges used up | $1.83 | 70 | 2 | `The exact value is not established; 0 ≤ b(d,k) ≤ d−2 for d ≥ 3 and k ≥ 1.` | no | not definite | no |
| p41 #6 | 20261120-141629-p41 | all agents idle, the nudges used up | $0.55 | 24 | 2 | none | no | no answer | no |
| p41 #7 | 20261120-144732-p41 | all agents idle, the nudges used up | $1.47 | 86 | 2 | `The exact value is undetermined; b(d,k) ≤ d−2 for d≥3 and k≥1.` | no | not definite | no |
| p41 #8 | 20261120-151253-p41 | all agents idle, the nudges used up | $0.63 | 30 | 2 | none | no | no answer | no |
| p43 #1 | 20261120-114859-p43 | all agents idle, the nudges used up | $0.32 | 13 | 2 | none | no | no answer | no |
| p43 #2 | 20261120-121321-p43 | all agents idle, the judge found the proof complete | $0.18 | 6 | 0 | `3` | no | sound | false stop |
| p43 #3 | 20261120-125303-p43 | all agents idle, the nudges used up | $1.04 | 34 | 2 | `The minimum is at most three; the sharp lower bound is not established.` | no | not definite | no |
| p43 #4 | 20261120-131905-p43 | all agents idle, the judge found the proof complete | $0.44 | 15 | 1 | `3` | no | sound | false stop |
| p43 #5 | 20261120-134447-p43 | all agents idle, the nudges used up | $0.45 | 18 | 2 | `The minimum is at most 3; the exact minimum is not established.` | no | not definite | no |
| p43 #6 | 20261120-142129-p43 | all agents idle, the judge found the proof complete | $0.58 | 19 | 1 | `3` | no | gap | no |
| p43 #7 | 20261120-144952-p43 | all agents idle, the nudges used up | $0.72 | 25 | 2 | `The minimum is at most 3; the exact minimum is not established.` | no | not definite | no |
| p43 #8 | 20261120-151253-p43 | all agents idle, the nudges used up | $0.49 | 18 | 2 | `The minimum is at most three; whether one or two fixed points are possible remains unresolved.` | no | not definite | no |
| p48 #1 | 20261120-115420-p48 | all agents idle, the nudges used up | $0.93 | 31 | 2 | `For all sufficiently large j, 2 ≤ κ(U_j) ≤ 3; the limit has not been determined.` | no | not definite | no |
| p48 #2 | 20261120-121901-p48 | all agents idle, the nudges used up | $0.52 | 19 | 2 | none | no | no answer | no |
| p48 #3 | 20261120-125623-p48 | all agents idle, the nudges used up | $1.70 | 49 | 2 | `\(\displaystyle\lim_{j\to\infty}\kappa(U_j)=3\).` | yes | sound | yes |
| p48 #4 | 20261120-132606-p48 | all agents idle, the nudges used up | $1.29 | 42 | 2 | `For every j, 2 ≤ κ(U_j) ≤ 3. The requested limit is not determined.` | no | not definite | no |
| p48 #5 | 20261120-134527-p48 | all agents idle, the nudges used up | $0.75 | 28 | 2 | `For every j, 2 ≤ κ(U_j) ≤ 3. The limit remains undetermined.` | no | not definite | no |
| p48 #6 | 20261120-142250-p48 | all agents idle, the nudges used up | $0.71 | 25 | 2 | `For every j, 2 ≤ κ(U_j) ≤ 3. Convergence and the value of the limit remain undetermined.` | no | not definite | no |
| p48 #7 | 20261120-145012-p48 | all agents idle, the nudges used up | $0.45 | 17 | 2 | `For every j, 2 ≤ κ(U_j) ≤ 3; the limit remains undetermined.` | no | not definite | no |
| p48 #8 | 20261120-151454-p48 | all agents idle, the nudges used up | $0.81 | 28 | 2 | `For every j, 2 ≤ κ(U_j) ≤ 3. The requested limit remains undetermined.` | no | not definite | no |

Solved 22 of 72 ended runs (9 problems); 4 of 9 problems solved by at least one run: 22 right answers, 25 stops (3 on a wrong answer). The agents cost $52.15, reading them $5.13.
