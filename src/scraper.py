import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests
import sys



class tableScraper():
    def get_header(self,table):
        header=[]
        header_chunks=table.find_all('th')
        sample=[]
        for i in header_chunks:
            value=[i.get_text().strip('\n').replace(',', '-')]
            sample=np.concatenate((sample, value), axis=0)
        header.append(sample)
        return(header)
    def get_data(self,table,div,clase):
        data=[]
        indexes=table.find_all(div,{"class":clase})
        for i in indexes:
            branch=i.find_previous("tr")
            childs=branch.find_all('td')
            sample=[]
            for j in range(0,len(childs)):
                value=[childs[j].get_text().strip('\n').replace(',', '')]
                sample=np.concatenate((sample, value), axis=0)
            if(sample==[] or sample[-1]==''):
                continue
            data.append([sample])
        return data
    def create_dataset(self,data,header):
        df=pd.DataFrame(np.concatenate(data),columns=header)
        return(df)
    def save_data(self,file,name,sep):
        file.to_csv('../datasets/'+name+'.csv',sep=sep)


class graphScraper():
    def __init__(self):
        self.months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    def __appendseries(self,dictionary,df):      
        keys=dictionary.keys()
        for i in keys:
            df=df.append(dictionary[i], ignore_index=True)
        return(df,keys)
    
    def __sort_days(self,days):
        sort_response=[]
        for i in self.months:
            month_days = list(filter(lambda x: i in x, days)) 
            sort_response=sort_response+month_days
        return(sort_response)
    def get_series(self,table,div,clase,attr,url):
        data_complete=dict()
        paths=[]
        countries=[]
        total_days=[]
        seeds=table.find_all(div,{"class":clase})
        for i in seeds:
            countries.append(i.find_all(text=True))
            paths.append(i.attrs[attr])
        for i,country in zip(paths,countries):
            page=requests.get(url+'/'+i)
            soup=BeautifulSoup(page.content,features="lxml")
            graph=soup.find('div',{"id":'graph-cases-daily'}).parent
            script=graph.find('script', type='text/javascript')
            js: str = script.text.replace('\n', '')
            patterns=re.findall(r'\[.*?]',js)
            days=patterns[0]
            days=days.replace('"', '')
            days=days.replace('[', '')
            days=days.replace(']', '')
            days=days.split(',')
            data=patterns[1]
            data=re.search(r'\[(.*?)\]',data).group(1).split('[')[1]
            data=data.split(',')
            total_days=total_days + days
            total_days=np.unique(total_days).tolist()
            ziplist = zip(days, data)
            data_complete[country[0]]=dict(ziplist)

        return(np.unique(total_days).tolist(),data_complete)
    

    def create_series_dataset(self,total_days,data_complete):
        days_sorted=self.__sort_days(total_days)
        df_data=pd.DataFrame(columns=days_sorted)
        data,countries=self.__appendseries(data_complete,df_data)
        data.index=countries
        data=data.T
        data=data.fillna(0)
        data=data.replace('null',0)
        return(data)



    def save_data(self,file,name,sep):
        file.to_csv('../datasets/'+name+'.csv',sep=sep)
    
     