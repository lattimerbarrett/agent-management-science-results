from pathlib import Path
p=Path('experiments/e1/agent3_qt_ultraproduct_notes.md')
print(p.read_text())
print('\nUniformity argument: if tau(b_k-a_k)>=epsilon and tau(b_k)-tau(a_k)->0,')
print('the ultraproduct has A<=B, q(B-A)>=epsilon, and q(A)=q(B).')
print('Faithfulness gives A!=B, contradicting verified strict order preservation.')