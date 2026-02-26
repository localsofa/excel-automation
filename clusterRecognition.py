# library setup guide in terminal

# spacy
# pip install -U pip setuptools wheel
# pip install -U spacy
# python -m spacy download de_core_news_sm

# pandas
# pip install pandas



"""Recognition of clusters in bisyllabic / monosyllabic words in German.
- Syllable recognition
- Cluster recognition
- Error of grammatical gender returned as 1 (false) or 0 (true) (not done yet)"""



# oder spaCy vielleicht für geschlechtserkennung? wenn spaCy und daten zusammenstimmen = 0, wenn nicht = 1
# später: "spaCy sagt zB männlich (spalte 1); person sagte aber weiblich (spalte 2) --> wenn beide übereinstimmen = 0, wenn nicht = 1"


import spacy
import pandas as pd
from spacy_syllables import SpacySyllables

nlp = spacy.load("de_core_news_sm")    
nlp.add_pipe("syllables", after="tagger")


# read excel file
sentences = pd.ExcelFile("nounsNrules.xlsx")
sheetname = "Sheet1"
df = pd.read_excel(sentences, sheetname, header = 0)

print("file read")

# syllables
def get_syllable_count(word):
    doc = nlp(word)
    if len(doc) > 0:
        return doc[0]._.syllables_count
    return 0

df["syllableCount"] = df["compound"].apply(get_syllable_count)

print("syllables done")

# MONOSYLLABIC INITIAL CLUSTERS
def get_word_initial_cluster(row):
    syllable_count = row['syllableCount']
    word = row['compound'].lower()
    
    clusters = ["schl", "schm", "schn", "schr", "schw", "dr", "fl", "fr", "gr", "kl", "kn", "kr", "sp", "st", "tr"]
    
    if syllable_count == 1:
        for cluster in clusters:
            if word.startswith(cluster):
                return cluster
    return ""

df["wordInitial"] = df.apply(get_word_initial_cluster, axis=1)

print("monosyllabic clusters done")


# BISYLLABIC ENDING SCHWA
def get_schwa(row):
    syllable_count = row['syllableCount']
    word = row['compound'].lower()
    
    clusters = ["e"]
    
    if syllable_count == 2:
        for cluster in clusters:
            if word.endswith(cluster):
                return "yes"
    return ""

df["schwa"] = df.apply(get_schwa, axis=1)

print("bisyllabic end schwa done")

dfNoGaps = df.drop(df[(df['wordInitial'] == "") & (df['schwa'] == "")].index)

print("gaps gone!")


# final save
# df.to_excel("corpusFinal.xlsx", index = False)
dfNoGaps.to_excel("corpusFinal.xlsx", index = False)

print("done!")

