from pathlib import Path
p=Path('workspace/agent3_uniform_imbalance_lemma.md')
s=p.read_text()
old='For completeness the truncation is uniform: while j<=epsilon*n, the analytic saddle and factorial ratios give a coarse ratio <=(C_r/n)^j for a fixed small epsilon>0, and S_j<=2^j binom(M,j) yields a factorial tail C^j/j!. For j>=epsilon*n the elementary factorial contraction bound gives n^(-epsilon*n)exp(O(n)), negligible relative to the Hamilton scale n!q^n exp(-o(n)); there are only exp(O_D(n)) edge subsets. This justifies truncating at log n and all termwise estimates.'
new='The uniform joint omission/contraction factorial tail is proved below using the ORIGINAL fixed tilt. It justifies truncating j at log n, without any estimate depending on the part proportions after omissions.'
assert old in s;s=s.replace(old,new)
old='The omission tail is genuinely uniform even for delta=o(n): for D_0<=epsilon*n both the original and reduced proportions remain in the fixed saddle neighborhood, and saddle/factorial ratios give <=(C/n)^(D_0). Multiplication by choices of omitted vertices gives <=C^(D_0)/product d_i!, hence the sum beyond log n is superpolynomially small. For D_0>=epsilon*n, the crude cycle bound n^(n-D_0) is exp(-Omega(n log n)) smaller than the Hamilton scale. This also handles induced internal graphs, whose degree remains <=D.'
new='''Here is a single genuinely UNIFORM joint tail bound, including when omissions make the induced part proportions highly unbalanced. Keep the original tilt t=t(p), and put rho_i=exp(t_i)/lambda(t). Nonnegative coefficient extraction gives the upper bound

 W(n-b-j, a-b-j) <= r*lambda(t)^(n-b-j)*exp(-t.(a-b-j)),

where W is the rooted proper-word coefficient, b=sum b_i counts omitted vertices and j=sum j_i internal contracted edges. The denominator W(n,a) is bounded below by a constant times n^(-(r-1)/2)*lambda(t)^n*exp(-t.a), by (S). After choosing omissions, the exact factorial-label ratio is

 product_i 1/[b_i!*(a_i-b_i)_{j_i}].

In an induced part of size a_i-b_i, the weighted j_i-edge linear-forest count is at most [D*(a_i-b_i)]^j_i/j_i!, since there are at most D*(a_i-b_i)/2 edges and orientation weight is at most 2^j_i. For every A>=j, the descending factorial satisfies (A)_j >=(A/e)^j: the geometric mean of the top j factors is at least that of A!, which is at least A/e. Thus the complete joint contribution divided by the original Hamilton kernel is at most

 n^C * product_i [rho_i^b_i/b_i!]*[(D*e*rho_i)^j_i/j_i!].

The polynomial includes rooting-length ratios (at most n) and harmless exceptional contracted words of length two. All-internal cycles have only bounded length in the bounded-component application, and are negligible on the Hamilton scale. The rho_i stay in a fixed compact positive interval, so the sum where b or j exceeds log n is superpolynomially small. This establishes the uniform joint tail, permits every preceding termwise saddle expansion, and needs no balancing assumption on induced subsets.'''
assert old in s;s=s.replace(old,new)
old='Apply (U) to the original graph and this competitor. The internal edge terms differ by O_H((1+||delta||)/n).'
new='Apply (U) to the original graph and this competitor. The ORIGINAL minus COMPETITOR internal-edge term is at most O_H((1+||delta||)/n), using M<=rho*n_active+O_H(1) and M_bal>=rho*n_active,balanced-O_H(1). This is a ONE-SIDED bound, which is all maximality needs; absolute control would require the already-repacked efficient forest.'
assert old in s;s=s.replace(old,new)
p.write_text(s)
print('Updated own uniform lemma with joint fixed-tilt tail and one-sided M comparison.')
