import pandas as pd
import os
import pyLDAvis
import pyLDAvis.gensim
from collections import Counter
import numpy as np
import spacy
import gensim
import en_core_web_sm as encore
nlp = encore.load()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from dateutil.parser import parse
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from pattern.en import lemma
from gensim import models,corpora
from gensim.utils import simple_preprocess


# In[266]:


df=pd.read_pickle(r"C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl")
directory = r"C:\Users\20311107\env_site\Scripts\news\newsui"
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".csv"):
            #print(file)
            tmpdf=pd.read_csv(file)
            df=pd.concat([df, tmpdf])
            df=df.drop(columns='Unnamed: 0')
            df.fillna('',inplace=True)
df=df.drop_duplicates(subset=['Link'])
df.to_pickle(r'C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl')
for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            os.remove(file)
df[['Heading','Text','Summary','Date']]=df[['Heading','Text','Summary','Date']].apply(lambda x:x.apply(lambda y:y.replace('\n','').replace('\t','').replace('\r','')))
df['Date']=df['Date'].apply(lambda x:x.replace('Last Updated','').replace('at','').replace('on','').strip())
df['Heading']=df['Heading'].str.strip()
df.Date=df.Date.apply(lambda x:x.split('(',1)[0])
df.Date=df.Date.apply(lambda x: x[1:] if x[0]==':' else x)
df.Date=df.Date.apply(lambda x:parse(x).date())
df=df[df.Text!=""]
print(len(df))
df['Text_token']=df.Text.apply(lambda x:simple_preprocess(x, deacc=True))
df.Text_token=df.Text_token.apply(lambda x:[z for z in x if z not in ENGLISH_STOP_WORDS])
bigram = models.Phrases(df.Text_token, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = models.Phrases(bigram[df.Text_token], threshold=100)  
# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = models.phrases.Phraser(bigram)
trigram_mod = models.phrases.Phraser(trigram)
#Making Bigrams
df.Text_token=df.Text_token.apply(lambda x:bigram_mod[x])
#Making Trigrams
df.Text_token=df.Text_token.apply(lambda x:trigram_mod[bigram_mod[x]])
df.Text_token=df.Text_token.apply(lambda x:[lemma(wd) for wd in x])
df.Text_token=df.Text_token.apply(lambda x:" ".join(x))

tmpdf=df#.sample(frac=0.2)
defencelst=[' ship ',' ships ','nuclear','drone','submarine','propulsion','sea machine','defence ministry','destroyer',            'combat suit','vessel','shipyard','shipbuilding','naval','gun','warship','marine','radar','bridge',            'ministry of defence',' mod ','(mod)',' dod ','(dod)','lithium','lithium-ion',' aip ','sonar',            'department of defence','uk mod','u.k. mod','us dod','u.s. dod','ministries of defense',            'artificial intelligence','a.i.','digital twin',' roe ','rubin','indian navy','indegenize','make in india',            'atmanirbhar bharat','atmanirbhar','defense export','defense procurement',' gst ',' idex ',            'defense start-up','defense budget','predictive maintainence','defense startup','lada-class',            'mazagon','tkms','dmse','thyssenkrupp','daewoo','rdel','p75','p75i','rfp',' aon ','ssbn','ssn'            'atvp','arihant','arighat','astute','virginia','scorpene',' lada ','drdo','amur','barracuda'            'kss','s80']
political_lst=[' mod ','(mod)','ministry of defence','ministries of defence','uk mod','u.k. mod','us dod',               'u.s. dod','department of defense','defense ministry',' dod ','(dod)'             'ministry of defence','indian navy','indegenize','make in india','atmanirbhar bharat']
economic_lst=[' mod ','ministry of defence','uk mod','u.k. mod','us dod','department of defense',             'ministry of defence','(mod)','ministries of defence','defence export','u.s. dod',              'defense procurement',' gst ',' idex ','atmanirbhar',' dod ','(dod)'             'indian navy','make in india','defense start-up','defense budget','indegenize','atmanirbhar bharat',]
technology_lst=['lithium','lithium-ion','battery','air-independent propulsion',' aip ','sonar','combat suit',               'a.i.'," ai ",'machine learning','digital twin','predictive maintainence','defense startup',               'artificial intelligence']
collab_lst=['naval group',' roe ','rubin','navantia','tkms','dsme','thyssenkrupp','daewoo']
competitor_lst=['mazagon dock shipbuilder','mazagon','reliance defence and engineering limited'," rdel "]
p75_lst=['p75','p75i','rfp',' aon ','acceptance of necessity']
submarine_lst=['submarine','conventional submarine','ssbn','ssn','submersible ship nuclear',               'submersible ship ballistic missile nuclear','atvp','vessel','submarine','arihant',               'arighat','astute','virginia','scorpene',' lada ','lada class','lada-class','amur',               'sea machine','barracuda','s80','kss']
lst=[]
entity_dict_full={"LOC":[],"NORP":[],"GPE":[],"ORG":[],"NORP":[],"PERSON":[],"PRODUCT":[],"DEFENCE":[],                 "POLITICAL":[],"ECONOMIC":[],"TECHNO":[],"COLLAB":[],"COMPET":[],"P75":[],"SUBMARINE":[]}
for i in range(len(tmpdf)):    
    doc = nlp(tmpdf.iloc[i].Summary.lower())
    strdoc = tmpdf.iloc[i].Summary.lower()
    entity_dict={"LOC":[],"NORP":[],"GPE":[],"ORG":[],"NORP":[],"PERSON":[],"PRODUCT":[],"DEFENCE":[],                 "POLITICAL":[],"ECONOMIC":[],"TECHNO":[],"COLLAB":[],"COMPET":[],"P75":[],"SUBMARINE":[]}
    for ent in doc.ents: 
        #print(ent.text,ent.label_)
        if ent.label_ in entity_dict.keys() and ent.text not in entity_dict[ent.label_]:
            entity_dict[(ent.label_)].append(ent.text)
            entity_dict_full[(ent.label_)].append(ent.text)
    for j in defencelst:
        if j in strdoc and j not in entity_dict["DEFENCE"]:
            entity_dict["DEFENCE"].append(j)
            entity_dict_full["DEFENCE"].append(j)
    for j in political_lst:
        if j in strdoc and j not in entity_dict["POLITICAL"]:
            entity_dict["POLITICAL"].append(j)
            entity_dict_full["POLITICAL"].append(j)
    for j in economic_lst:
        if j in strdoc and j not in entity_dict["ECONOMIC"]:
            entity_dict["ECONOMIC"].append(j)
            entity_dict_full["ECONOMIC"].append(j)
    for j in technology_lst:
        if j in strdoc and j not in entity_dict["TECHNO"]:
            entity_dict["TECHNO"].append(j)
            entity_dict_full["TECHNO"].append(j)
    for j in collab_lst:
        if j in strdoc and j not in entity_dict["COLLAB"]:
            entity_dict["COLLAB"].append(j)
            entity_dict_full["COLLAB"].append(j)
    for j in competitor_lst:
        if j in strdoc and j not in entity_dict["COMPET"]:
            entity_dict["COMPET"].append(j)
            entity_dict_full["COMPET"].append(j)
    for j in p75_lst:
        if j in strdoc and j not in entity_dict["P75"]:
            entity_dict["P75"].append(j)
            entity_dict_full["P75"].append(j)
    for j in submarine_lst:
        if j in strdoc and j not in entity_dict["SUBMARINE"]:
            entity_dict["SUBMARINE"].append(j)
            entity_dict_full["SUBMARINE"].append(j)
    #print(tmpdf.iloc[i].Summary.lower())        
    #print(entity_dict)
    lst.append(entity_dict)
    #print("------------")

tmpdf['Entity']=lst
for i in entity_dict_full.keys():
    counts = Counter(entity_dict_full[i])
    print(i,"\n",counts,"\n")


#tmpdf.apply(lambda x:print("\n",x.Heading,"\n",x.Summary,x.Entity) if len(x.Entity['DEFENCE'])>2 else None,axis=1)
#tmpdf.apply(lambda x:print("\n",x.Heading,"\n",x.Summary,x.Entity) if 'virginia' in x.Entity['SUBMARINE'] else None,axis=1)

