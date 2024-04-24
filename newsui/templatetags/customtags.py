from django import template 
register = template.Library() 
from ..models import article
import pandas as pd

@register.filter 
def split(value,key): 
    return value.split(key)
    
@register.filter 
def replacestr(value,key): 
    return value.replace(key,'_')
    
@register.filter
def keywordfilter(value,key):
    tmp=pd.DataFrame()
    df=pd.read_pickle(r"C:\Users\87385816\Documents\News_Clustering\news\newsui\newsdata.pkl")
    tmp=df[df.apply(lambda x:value in x.Entity['LOC'],axis=1)]
    tmp=pd.concat([tmp, df[df.apply(lambda x:value in x.Entity['ORG'],axis=1)]])
    tmp=pd.concat([tmp, df[df.apply(lambda x:value in x.Entity['GPE'],axis=1)]])
    tmp=pd.concat([tmp, df[df.apply(lambda x:value in x.Entity['PERSON'],axis=1)]])
    tmp=pd.concat([tmp, df[df.apply(lambda x:value in x.Entity['NORP'],axis=1)]])
    tmp=tmp[['Heading', 'Link', 'Image', 'Summary','Date']]
    article_list=[]
    for i in tmp.values:
        a=article()
        a.title,a.img,a.lnk,a.summary,a.date=i[0],i[2],i[1],i[3][:500],i[4]
        article_list.append(a)
    return article_list