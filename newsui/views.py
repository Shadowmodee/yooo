from django.shortcuts import render
from django.http import HttpResponse 
from .models import article
import pandas as pd
import os
from collections import Counter
import numpy as np
import spacy
import gensim
import en_core_web_sm as encore
nlp = encore.load()
from dateutil.parser import parse
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from pattern.en import lemma
from gensim import models,corpora
from gensim.utils import simple_preprocess
from wordcloud import WordCloud
from matplotlib import pyplot as plt 

df=pd.read_pickle(r"C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl")
print('original df',len(df))
directory = r"C:\Users\87385816\Documents\News_Clustering\news\newsui"
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".csv"):
            tmpdf=pd.read_csv(directory+("\\")+file)
            print('tmp',len(tmpdf))
            df=pd.concat([df, tmpdf])
            df=df.drop(columns='Unnamed: 0')
            df.fillna('',inplace=True)
df=df.drop_duplicates(subset=['Link'])
for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            os.remove(directory+("\\")+file)
df[['Heading','Text','Summary','Date']]=df[['Heading','Text','Summary','Date']].apply(lambda x:x.astype(str))
df[['Heading','Text','Summary','Date']]=df[['Heading','Text','Summary','Date']].apply(lambda x:x.apply(lambda y:y.replace('\n','').replace('\t','').replace('\r','')))
df['Date']=df['Date'].apply(lambda x:x.replace('Last Updated','').replace('Updated','')\
.replace('at','').replace('on','').strip())
df['Heading']=df['Heading'].str.strip()
df.Date=df.Date.apply(lambda x:x.split('(',1)[0])
df.Date=df.Date.apply(lambda x: x[1:] if x[0]==':' else x)
df.Date=df.Date.apply(lambda x:parse(x).date())
df=df.sort_values(by=['Date'],ascending=False)
df.Summary=df.Summary.apply(lambda x:'' if x=='nan' else x)
df=df[df.Summary!=""]
df=df[df.Image!=""]


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
df.to_pickle(r'C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl')
print('updated df',len(df))
defence=[' ship ',' ships ','nuclear','drone','submarine','propulsion','sea machine','defence ministry','destroyer','combat suit','vessel','shipyard','shipbuilding','naval','gun','warship','marine','radar','bridge','ministry of defence',' mod ','(mod)',' dod ','(dod)','lithium','lithium-ion',' aip ','sonar','department of defence','uk mod','u.k. mod','us dod','u.s. dod','ministries of defense','artificial intelligence','a.i.','digital twin',' roe ','rubin','indian navy','indegenize','make in india','atmanirbhar bharat','atmanirbhar','defense export','defense procurement',' gst ',' idex ','defense start-up','defense budget','predictive maintainence','defense startup','lada-class','mazagon','tkms','dmse','thyssenkrupp','daewoo','rdel','p75','p75i','rfp',' aon ','ssbn','ssn','atvp','arihant','arighat','astute','virginia','scorpene',' lada ','drdo','amur','barracuda','kss','s80']
political=[' mod ','(mod)','ministry of defence','ministries of defence','uk mod','u.k. mod','us dod','u.s. dod','department of defense','defense ministry',' dod ','(dod)','ministry of defence','indian navy','indegenize','make in india','atmanirbhar bharat']
economic=[' mod ','ministry of defence','uk mod','u.k. mod','us dod','department of defense','ministry of defence','(mod)','ministries of defence','defence export','u.s. dod','defense procurement',' gst ',' idex ','atmanirbhar',' dod ','(dod)','indian navy','make in india','defense start-up','defense budget','indegenize','atmanirbhar bharat']
technology=['lithium','lithium-ion','battery','air-independent propulsion',' aip ','sonar','combat suit','a.i.'," ai ",'machine learning','digital twin','predictive maintainence','defense startup','artificial intelligence']
collab=['naval group',' roe ','rubin','navantia','tkms','dsme','thyssenkrupp','daewoo']
competitor=['mazagon dock shipbuilder','mazagon','reliance defence and engineering limited'," rdel "]
p_75=['p75','p75i','rfp',' aon ','acceptance of necessity']
submarines=['submarine','conventional submarine','ssbn','ssn','submersible ship nuclear','submersible ship ballistic missile nuclear','atvp','vessel','submarine','arihant','arighat','astute','virginia','scorpene',' lada ','lada class','lada-class','amur','sea machine','barracuda','s80','kss']

def tagdata(defencelst,political,economic,technology,collab,competitor,p_75,submarines):
    tmpdf=pd.read_pickle(r"C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl")
    lst=[]
    entity_dict_full={"LOC":[],"NORP":[],"GPE":[],"ORG":[],"PERSON":[],"PRODUCT":[],"DEFENCE":[],\
    "POLITICAL":[],"ECONOMIC":[],"TECHNO":[],"COLLAB":[],"COMPET":[],"P75":[],"SUBMARINE":[]}
    for i in range(len(tmpdf)):    
        doc = nlp(tmpdf.iloc[i].Summary.lower())
        strdoc = tmpdf.iloc[i].Summary.lower()
        entity_dict={"LOC":[],"NORP":[],"GPE":[],"ORG":[],"PERSON":[],"PRODUCT":[],"DEFENCE":[],"POLITICAL":[],\
        "ECONOMIC":[],"TECHNO":[],"COLLAB":[],"COMPET":[],"P75":[],"SUBMARINE":[]}
        for ent in doc.ents: 
            #print(ent.text,ent.label_)
            if ent.label_ in entity_dict.keys() and ent.text not in entity_dict[ent.label_]:
                entity_dict[(ent.label_)].append(ent.text)
                entity_dict_full[(ent.label_)].append(ent.text)
        for j in defence:
            if j in strdoc and j not in entity_dict["DEFENCE"]:
                entity_dict["DEFENCE"].append(j)
                entity_dict_full["DEFENCE"].append(j)
        for j in political:
            if j in strdoc and j not in entity_dict["POLITICAL"]:
                entity_dict["POLITICAL"].append(j)
                entity_dict_full["POLITICAL"].append(j)
        for j in economic:
            if j in strdoc and j not in entity_dict["ECONOMIC"]:
                entity_dict["ECONOMIC"].append(j)
                entity_dict_full["ECONOMIC"].append(j)
        for j in technology:
            if j in strdoc and j not in entity_dict["TECHNO"]:
                entity_dict["TECHNO"].append(j)
                entity_dict_full["TECHNO"].append(j)
        for j in collab:
            if j in strdoc and j not in entity_dict["COLLAB"]:
                entity_dict["COLLAB"].append(j)
                entity_dict_full["COLLAB"].append(j)
        for j in competitor:
            if j in strdoc and j not in entity_dict["COMPET"]:
                entity_dict["COMPET"].append(j)
                entity_dict_full["COMPET"].append(j)
        for j in p_75:
            if j in strdoc and j not in entity_dict["P75"]:
                entity_dict["P75"].append(j)
                entity_dict_full["P75"].append(j)
        for j in submarines:
            if j in strdoc and j not in entity_dict["SUBMARINE"]:
                entity_dict["SUBMARINE"].append(j)
                entity_dict_full["SUBMARINE"].append(j)
        #print(tmpdf.iloc[i].Summary.lower())        
        #print(entity_dict)
        lst.append(entity_dict)
        #print("------------")

    tmpdf['Entity']=lst
    df=tmpdf
    df.to_pickle(r'C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl')
    return entity_dict_full
def home(request):
    checked_words = request.POST.getlist('checks')
    categories = request.POST.getlist('category')
    checked_words=[cw.replace('_',' ') for cw in checked_words]
    t,j,f_dict=[],0,{}
    for i in checked_words:
       if(i==":"):
        f_dict[categories[j]]=t
        t=[]
        j+=1
       else:
        t.append(i) 
    if len(f_dict):
        #print(f_dict)
        entity_dict_full=tagdata(list(f_dict.values())[0],list(f_dict.values())[1],list(f_dict.values())[2],\
                            list(f_dict.values())[3],list(f_dict.values())[4],list(f_dict.values())[5],\
                            list(f_dict.values())[6],list(f_dict.values())[7])
    else:
        entity_dict_full=tagdata(defence,political,economic,technology,collab,competitor,p_75,submarines)
    df=pd.read_pickle(r"C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl")
    df=df[df.apply(lambda x:len(x.Entity['DEFENCE'])>0 and (len(x.Entity['POLITICAL'])+\
                                            len(x.Entity['ECONOMIC'])+len(x.Entity['TECHNO'])+\
                                            len(x.Entity['COLLAB'])+len(x.Entity['COMPET'])+\
                                            len(x.Entity['P75'])+len(x.Entity['SUBMARINE']))>0,axis=1)]
    tmpdata=df.head(20)
    article_list=[]
    for i in tmpdata.values:#portion 0 -> Featured
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=0,i[0],i[2],i[1],i[3][:200],i[6]
        article_list.append(a)
    tmpdata=df[df.apply(lambda x:len(x.Entity['POLITICAL'])>0,axis=1)]
    for i in tmpdata.values:#portion 1-7 are user defined buckets
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=1,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    tmpdata=df[df.apply(lambda x:len(x.Entity['ECONOMIC'])>0,axis=1)]
    for i in tmpdata.values:
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=2,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    
    tmpdata=df[df.apply(lambda x:len(x.Entity['TECHNO'])>0,axis=1)]
    for i in tmpdata.values:
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=3,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    tmpdata=df[df.apply(lambda x:len(x.Entity['COLLAB'])>0,axis=1)]
    for i in tmpdata.values:
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=4,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    tmpdata=df[df.apply(lambda x:len(x.Entity['COMPET'])>0,axis=1)]
    for i in tmpdata.values:
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=5,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    tmpdata=df[df.apply(lambda x:len(x.Entity['P75'])>0,axis=1)]
    for i in tmpdata.values:
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=6,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    tmpdata=df[df.apply(lambda x:len(x.Entity['SUBMARINE'])>0,axis=1)]
    for i in tmpdata.values:
        a=article()
        a.portion,a.title,a.img,a.lnk,a.summary,a.date=7,i[0],i[2],i[1],i[3][:500],i[6]
        article_list.append(a)
    #Images Dynamic are in portion 8 bucket by loop
    for i in ['LOC','NORP','GPE','ORG','PERSON']:
        counts = Counter(entity_dict_full[i])
        #print(i,counts)
        tmplst=[]
        for j in counts.keys():
            if(counts[j]>1):
                #print(j,counts[j])
                tmplst.append(j)
        a=article()
        a.portion,a.title,a.summary=8,i,(':'.join(tmplst))
        article_list.append(a)
        wordcloud = WordCloud(width = 800, height = 800, background_color ='black',  min_font_size = 10).generate_from_frequencies(counts) 
        plt.figure(figsize = (8, 8), facecolor = None) 
        plt.imshow(wordcloud)
        plt.axis("off") 
        plt.tight_layout(pad = 0)   
        wordcloud.to_file(r'C:\Users\87385816\Documents\News_Clustering\news\static\img\\'+i+'.png')
    #Filter keywords dynamic
    tmpdict={'defence':defence,'political':political,'economic':economic,\
                            'technology':technology,'collab':collab,'competitor':competitor,\
                            'p_75':p_75,'submarines':submarines}
    for i in tmpdict.keys():
        a=article()
        a.portion,a.title,a.summary=9,str(i),(':'.join(tmpdict[i]))
        #print(i,tmpdict[i])
        article_list.append(a)
    return render(request,"index.html",{'articles':article_list})
    