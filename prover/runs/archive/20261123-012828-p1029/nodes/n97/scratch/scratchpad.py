from pathlib import Path
p=Path('experiments/e1/agent3_qt_ultraproduct_notes.md')
print(p.read_text())
print('\nSTRICTNESS TEST:')
print('For B=[a_n], C=[a_(n+1)] in the quasitracial ultrapower:')
print('  tau_U(B)=lim tau(a_n)=L=tau_U(C)')
print('  tau_U(C-B)=eta>0, hence 0 <= B < C.')
print('Strict order preservation in the finite AW*-factor ultrapower rules this out.')
