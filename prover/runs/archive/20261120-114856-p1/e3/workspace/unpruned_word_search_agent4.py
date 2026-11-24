from pathlib import Path
src=Path('workspace/word_search_agent4.py').read_text()
src=src.replace('def words(refs,side,depth=4):','def words(refs,side,depth=7):').replace('ivcont=constrain(ivn,side*MM[1])','ivcont=ivn')
src=src.replace('range(10000)','range(20000)').replace('case%50','case%1000').replace('word_search_agent4.py','unpruned_word_search_agent4.py').replace('words_found_agent4.pkl','unpruned_words_found_agent4.pkl')
exec(compile(src,'unpruned','exec'))
