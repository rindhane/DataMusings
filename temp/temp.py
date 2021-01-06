######polynomial trial 
#degree of polynomial of 3 was tested and 
#provide results with only power of 1
from downloader import get_data
df_dict=get_data()
listings=df_dict['listings']
calendar=df_dict['calendar']
reviews=df_dict['reviews']
from clean_data import clean_preprocess_listings
data=clean_preprocess_listings(listings)
##data downloaded , building model
import pandas as pd
from functions import subtract_elem
from model_functions import Pipeline,sklearn_model,ml_model_setup
pipe1 = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('regressor', AdaBoostRegressor(n_estimators=200, 
                                    loss='exponential')),
    ])
regressor = sklearn_model(model=pipe1)
model=ml_model_setup(data=None, model=regressor)

tmp=pd.get_dummies(data,columns=['neighbourhood_cleansed','bathrooms_type',
                                'room_type'],
                            prefix=['neighbourhoods','bathroom','room_type'],
                            prefix_sep='-')
outcomes=['annual_earnings']
variables=subtract_elem(tmp.columns,outcomes)
model.set_inputs(data=tmp,
                outcomes=outcomes,
                variables=variables)
model.train()
##model trained plotting results
import numpy as np
ans=model.model.model.named_steps.regressor.feature_importances_
order=ans.argsort()[::-1]
power_array=model.model.model.named_steps.poly.powers_[order]
print("The top 3 predicting variables are ")
for i in range(0,3):
    var = list(tmp[variables].columns[\
    np.nonzero(power_array[i])])
    powers=list(power_array[i][np.nonzero(power_array[i])])
    stat=""
    a=0
    for p,n in zip(var,powers):
        string= f"{p}{('^'+str(n)) if n > 1 else '' }"
        stat=stat+('*' + string) if a > 0 else string
        a=a+1
    print(f"{i+1} : "+stat)

########### external ip check function 
import requests
from bs4 import BeautifulSoup as bs
r=requests.get('https://www.whatismyip.com/')
print('status:',r.status_code)
soup=bs(r.content.decode(r.encoding),'html.parser')
soup.get_text()
for span in soup.find_all('span'):
    if 'cf-footer-item' in span.get_attribute_list('class'):
        for child in span.find_all('span'):
            if "Your IP" in child.get_text():
                print(span.get_text())

