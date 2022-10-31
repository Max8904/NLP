import re
from collections import Counter
from pprint import pprint
import streamlit as st

#from functools import filter

def words(text): return re.findall(r'\w+', text.lower())
word_count = Counter(words(open('big.txt').read()))
N = sum(word_count.values())
def P(word): return word_count[word] / N # float

#Run the function:

# print( list(map(lambda x: (x, P(x)), words('speling spelling speeling'))) )

letters    = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(1,len(word) + 1)]    # range(1,len(word) + 1)
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
    
#Run the function:
# pprint( list(edits1('speling'))[:3])
#pprint( list(map(lambda x: (x, P(x)), edits1('speling'))) )
#print( list(filter(lambda x: P(x) != 0.0, edits1('speling'))) )
#print( max(edits1('speling'), key=P) )

def correction(word): 
    if(re.match(r'^col[^l]',word)):
        word = word.replace('col','coll')
        return word
    if(re.match(r'.*aly$',word)):
        word = word.replace('ly','lly')
        return word
    if(re.match(r'.*aned$',word)):
        word = word.replace('ned','nned')
        return word
    if(re.match(r'.*aled$',word)):
        word = word.replace('led','lled')
        return word
    if(re.match(r'.*lys$',word)):
        word = word.replace('lys','lies')
        return word
    if(re.match(r'.*[^a]ble$',word)):
        word = word.replace('ble','able')
        return word
    if(re.match(r'.*tative$',word)):
        word = word.replace('tative','titive')
        return word
    if(re.match(r'.*sability$',word)):
        word = word.replace('sability','sibility')
        return word
    return max(candidates(word), key=P)

# def candidates(word): 
#     return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

set0 = {} 
set1 = {}
set2 = {}
set3 = {}
def candidates(word): 
    set0 = known([word])
    if set0:
        return set0
    else:       
        set1 = edits1(word)
        set1_known = known(set1)
        if set1_known:
            return set1_known
        else:        
            set2 = edits2(set1)
            set2_known = known(set2)
            if set2_known:
                return set2_known
            else:
                return [word]

def known(words): 
    return set(w for w in words if w in word_count)

def edits2(set1):
    return (e2 for e1 in set1 for e2 in edits1(e1))

vowel    = 'aeiou'
def edits3(set2):
    splits = []
    deletes = []
    transposes = []
    replaces = []
    inserts = []
    for word in set2:
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in vowel]
        inserts    = [L + c + R               for L, R in splits for c in vowel]
    return set(deletes + transposes + replaces + inserts)

# print('speling -->', correction('speling'))
# speling spelling

def spelltest(tests, verbose=True):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.time()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in word_count)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, word_count[w], right, word_count[right]))
    dt = time.time() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

# print(unit_tests())
# spelltest(Testset(open('spell-testset1.txt'))) # Development set
# spelltest(Testset(open('spell-testset2.txt'))) # Final test set



add_selectbox = st.sidebar.checkbox("Show original word")

st.title("Spellchecker Demo")
# option = st.selectbox("Choose a word or...",["","problem","juise","localy","level","basicaly","available","seperate","remind","ther","totally","between","awful"])

option = st.selectbox("Choose a word or...",["","apple","lamon","speling","hapy","language","greay","sussess"],help="You really need instructions for this?")

word = st.text_input("type your own!!", option, help="Type a word, any word.")
word_corrected = correction(word)

if(add_selectbox):
    st.markdown(f"Original word: {word}")

if(word!= ""):
    if(word == word_corrected):
        st.success(f'{word} is the correct spelling!')
    else:
        st.error(f'Correction: {word_corrected}')
