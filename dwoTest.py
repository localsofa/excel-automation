import spacy
import pandas as pd


nlp = spacy.load("de_core_news_sm")    

# read excel file
sentences = pd.ExcelFile("result.xlsx")
sheetname = "Sheet1"
df = pd.read_excel(sentences, sheetname, header = 0)

print("still going!")

def FV(sentence):
    doc = nlp(str(sentence))
    for token in doc:
        if "VerbForm=Fin" in token.morph:
            # token.dep_ for dependency label (e.g., 'aux', 'cop', etc.)
            return token.dep_
    return ""

print("almost done!")

def DWO(sentence):
    """
    - 'ppart': sentence contains an auxiliary and a past participle (VerbForm=Part).
    - 'inf': sentence contains a modal auxiliary and an infinitive (VerbForm=Inf).
    - 'particle': sentence contains a separable particle (dependency 'prt' or tag 'PTKVZ').
    - 'empty': only a finite verb (no non-finite part matching above rules).
    """
    doc = nlp(str(sentence))

    has_part = any("VerbForm=Part" in t.morph for t in doc)
    has_inf = any("VerbForm=Inf" in t.morph for t in doc)
    has_aux = any(t.pos_ == "AUX" for t in doc)

    # check lemma against common modal verbs
    modal_lemmas = {"können", "müssen", "dürfen", "sollen", "wollen", "mögen", "möchten"}
    has_modal_aux = any((t.pos_ == "AUX" or t.pos_ == "VERB") and (t.lemma_.lower() in modal_lemmas) for t in doc)

    # separable particle detection: dependency label 'prt' or tag 'PTKVZ'
    has_particle = any(t.dep_ == "prt" or t.tag_ == "PTKVZ" for t in doc)

    if has_part and has_aux:
        return "ppart"
    if has_inf and has_modal_aux:
        return "inf"
    if has_particle:
        return "particle"

    # if nothing, then empty
    return "empty"


df["verb"] = df["utterance"].apply(FV)
df["dwo"] = df["utterance"].apply(DWO)
df.to_excel("result.xlsx", index = False)

print ("done!")