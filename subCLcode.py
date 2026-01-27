# library setup guide in terminal

# spacy
# pip install -U pip setuptools wheel
# pip install -U spacy
# python -m spacy download de_core_news_sm

# pandas
# pip install pandas

import spacy
import pandas as pd

nlp = spacy.load("de_core_news_sm")    

# read excel file
sentences = pd.ExcelFile("SubClTest.xlsx")
sheetname = "SubCL"
df = pd.read_excel(sentences, sheetname, header = 0)

print("file read")

def get_last_conjunction(sentence):
    """Extract the first conjunction or relative pronoun from a sentence.
    
    Returns the text of the first conjunction (CCONJ, SCONJ) or relative pronoun (PRON with PronType=Rel).
    Returns empty string if no conjunction/relative pronoun found.
    """
    doc = nlp(str(sentence))

    # 1) Check for a pronoun at the start (ignore filler tokens that start with '&' or contain '@')
    for token in doc:
        t = token.text
        if not t or t.isspace():
            continue
        # skip filler tokens like '&laugh' or tokens containing '@'
        if t.startswith('&') or ('@' in t):
            continue
        # skip punctuation
        if token.is_punct:
            continue
        # if the first real token is a pronoun, return it
        if token.pos_ == 'PRON':
            return token.text
        # otherwise stop checking first-token behavior
        break

    # 2) Fallback: find first conjunction or relative pronoun anywhere in the sentence
    for token in doc:
        if token.pos_ in {'CCONJ', 'SCONJ'}:
            return token.text
        if token.pos_ == 'PRON' and 'PronType=Rel' in token.morph:
            return token.text

    return ""


df["conj"] = df["utterance"].apply(get_last_conjunction)
df.to_excel("SubCLFinal.xlsx", index = False)

print ("done!")
