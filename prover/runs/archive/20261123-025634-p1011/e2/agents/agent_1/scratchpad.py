from pathlib import Path
files=['agent2_n21_finite_lemma_complete.txt','agent4_uniform_graph_LS_theorem.txt','agent3_geometry_full_proof.txt']
head='''INTEGRATED DIMENSION-21 CONSTRUCTION UNDER THE EXPLICIT AMBIENT-LCF DEFINITION\n\nThe finite lemma gives a degree-six polynomial f in dimension20 with strict full\nshape-norm maximum. The uniform graph theorem applies because21>17 and yields\none fixed smooth graph F and exact nonnegative finite-energy solutions. The\ngeometry/regularity lemma compactifies this to one fixed smooth compact connected\n(M^21,g), locally conformally flat in the explicit ambient sense, positive Yamabe\ntype, nonhemisphere, with smooth strictly positive solutions and boundary suprema\ntending to infinity. Thus the COMPOSITION asserts21 in D, contrary to the stated\nD={n>=25}. All three complete proof pieces and code are included below so a\nconcrete error can be identified rather than concealed by a false compactness lemma.\n\n'''
text=head+'\n\n'.join(Path('workspace',name).read_text() for name in files)
text+='\n\nSTANDALONE EXACT FINITE CERTIFICATE\n\n'+Path('workspace/agent2_n21_standalone_certificate.py').read_text()
Path('workspace/agent1_integrated_n21_construction.txt').write_text(text)
print('Integrated proof and certificate:',len(text.splitlines()),'lines,',len(text),'characters')
