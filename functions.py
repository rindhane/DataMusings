#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pandas as pd 
from io import BytesIO
from gzip import GzipFile

def get_html(url):
    '''function to obtain html as bs4 object'''
    req=requests.get(url)
    if req.status_code == 200:
        r = req.content
        soup=bs(r.decode(),'html.parser')
        return soup
    else: 
        raise ValueError ("Can't access the the provided url.\
                            Check either the internet or url value")

def get_city(table):
    '''function to get city out of html table in bs4 objct'''
    return table.contents[3].tr.find_all('td')[1].text

def get_date(datetag):
    '''string to date conversion for text in tables''' 
    return datetime.strptime(datetag.text,"%d %B, %Y")

def details(table,date,types_req):
    '''function to get individual csv links from the desired city table''' 
    #type of filename required
    ans=list()
    for tr in table.contents[3].find_all('tr'):
        ld=list()
        td_list = tr.find_all('td')
        if td_list[0].text=='N/A' or get_date(td_list[0]) >= date :
            if td_list[2].text in types_req:
                ld.extend([td_list[0].text,
                        td_list[1].text,
                        td_list[2].a.get('href') ,
                        td_list[2].text.split('.')[0]] )
                ans.append(ld)
        else:
            break
    return ans

def get_tables(soup,types_req,city,date):
    "function to find the table of the given city"
    ref_date = datetime.strptime(date, '%b-%d-%Y') 
    for table in soup.find_all('table'):
        if get_city(table)==city:
            return details(table,ref_date,types_req)
    raise ValueError("City was not found")


def get_dataFrame(url:str) -> pd.DataFrame:
    '''function to get datafrom the link of the csv file'''
    req=requests.get(url)
    if req.status_code == 200:
        return pd.read_csv(GzipFile(fileobj=\
                            BytesIO(requests.get(url).content), 
                            mode='rb'))
    else: 
        raise ValueError ("Can't access the the provided url.\
                            Check either the internet or url value")


def get_data():
    url='http://insideairbnb.com/get-the-data.html'
    types_req = [
        'listings.csv.gz',
        'calendar.csv.gz',
        'reviews.csv.gz',
    ]
    tables=get_tables(get_html(url),
                        types_req=types_req,
                        date="Oct-01-2020",
                        city="Amsterdam",)
    df_dict=dict()
    for dt in types_req:
        check=dt.split('.')[0]
        for table in tables:
            if check in table:
                if not(type(df_dict.get(check,None))==None):
                    df_dict[check]=pd.concat(df_dict[check],
                                                get_dataFrame(table[2]),)
                else:
                    df_dict[check]=get_dataFrame(table[2])
    return df_dict