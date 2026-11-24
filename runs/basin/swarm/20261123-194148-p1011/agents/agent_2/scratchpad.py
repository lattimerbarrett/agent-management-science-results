from pathlib import Path
p=Path('workspace/agent2_local_sign_lemma.md')
x=p.read_text()
x=x.replace('The remaining correction q_i obeys\n\n ||q_i||_D<=o_i(eta_i)+C b_i r^theta+o_i(b_i).                              (B2)', 'The remaining correction first obeys the COARSE bound\n\n ||q_i||_D<=o_i(eta_i)+C_r b_i.                                           (B2c)\n\nOnly AFTER C3 has forced physical jetvanishing do cutoff-profile tail terms become\no_i(b_i) for fixed r, improving this to the REFINED bound\n\n ||q_i||_D<=o_i(eta_i)+C b_i r^theta+o_i(b_i).                              (B2r)')
x=x.replace('Pairing q with the source\nuses B2 and Young, costing a small multiple of eta_i^2 plus C b_i^2r^(2theta).', 'Pairing q with the source\nuses B2c and Young at the coarse stage, costing a small multiple of eta_i^2 plus\nC_r b_i^2. Only after C3/jetvanishing does B2r improve this cost to\na small multiple of eta_i^2 plus C b_i^2r^(2theta)+o_i(b_i^2).')
x=x.replace('The core low-jet nonlinear error remains absorbed in Q_i;', 'Now use the REFINED correction bound B2r; it has not been used to establish C3.\nThe core low-jet nonlinear error remains absorbed in Q_i;')
p.write_text(x)
print('Staging corrected: coarse B2c used before C3; B2r only after jetvanishing.')
