#! /usr/bin/env ipython
'''main file to execute the project'''

#downloading data into memory
from downloader import get_data
df_dict=get_data()
listings=df_dict['listings']
calendar=df_dict['calendar']
reviews=df_dict['reviews']

#cleaning & preprocessing the data
from clean_data import clean_preprocess_listings
data=clean_preprocess_listings(listings)
#plotting the results from the exploratory analysis

#results1 : Broad understanding of earning & avg.price

#results 2/ plot1:  various listings
from plot_functions import plot_graph
from functions import range_without_outliers
inputs= {
    'kind' : 'hist',
    'bins' : 200,
    'x_label' : 'Listings Prices in Boston',
    'y_label': "No. of Listings", 
    'labelsize': 20,
    'fontsize' : 30,
    'xlim':range_without_outliers(data['price']),
    'legendlabel':'price vs demand',
    'legendsize':20,
    'file_': 'results/price_demand.jpg'
}
plot_graph(data['price'].values, **inputs)

#results3 : Variation of avg.price & annual_earning across areas
from plot_functions import plot_graph_doubleX
tmp1=data[['neighbourhood_cleansed',
     'annual_earnings']].groupby(['neighbourhood_cleansed']).mean()
tmp2=data[['neighbourhood_cleansed',
     'price']].groupby(['neighbourhood_cleansed']).mean()
inputs={
    'title':'Annual Earning & Price/Night variation across Boston areas',
    'x_label':'Avg. annual_earnings',
    'y_label':'Areas in Boston',
    'kind':'barh',
    'x_label2': 'Avg.price/night',
    'figWidth':20,
    'figHeight':30,
    'labelsize':30,
    'fontsize':30,
    'legendsize':20,
    'legendlabel':'annual earning',
    'legendlabel2': 'price',
    'file_': 'results/earning_distribution.jpg'
    }
plot_graph_doubleX([tmp1.index.values,tmp1.values.flatten()],
          [tmp2.values.flatten(),tmp2.index.values,], 
           **inputs)

#results4 : Demand against different types of listings
from plot_functions import plot_graph_doubleY
from clean_data import categorical_values_rooms
from functions import reverse_dict,category_from_encoding
categories=reverse_dict(categorical_values_rooms(None,get_encoding=True))
tmp=data[['number_of_reviews_ltm','room_type','price']]
tmp=tmp.apply(lambda col : col.apply(category_from_encoding,args=(categories,))\
                     if col.name=='room_type' else col)
tmp1=tmp[['number_of_reviews_ltm','room_type']].groupby(['room_type']).mean()
tmp2=tmp[['price','room_type']].groupby(['room_type']).mean()
inputs={
    'title':'Avg. Annual demand for types of Listings',
    'y_label':'Avg No.of Vists per year',
    'x_label':'Types of Listings',
    'kind':'bar',
    'y_label2': 'Avg.price per night',
    'figWidth':20,
    'figHeight':30,
    'labelsize':30,
    'fontsize':30,
    'legendsize':20,
    'legendlabel':'Visits',
    'legendlabel2': 'price',
    'xlabelrotation':45,
    'file_': 'results/categorical_demand.jpg'
    }
plot_graph_doubleY([tmp1.index.values,tmp1.values.flatten()],
          [tmp2.index.values,tmp2.values.flatten()], 
           **inputs)

#results5 : Impact on vists from other parameters
cols=['instant_bookable','host_response_time',
    'host_descriptions',]
from plot_functions import plot_graph
tmp=data[cols+['number_of_reviews_ltm']]
labels={
    'instant_bookable' : {1:"yes",0:'no'},
    'host_response_time': {24:'within a day' ,  
                           8:'within a few hours' , 
                           1:'within an hour' ,
                           24*3:'a few days or more',
                           0: 'Non-responsive'}, 
    'host_descriptions':{6:'some',7:'enough',8:'good',9:'great'},
}
props={
    'instant_bookable': ['instant booking ','instant_impact.jpg' ],
    'host_response_time':['Host time to respond','host_response.jpg'],
    'host_descriptions':['more transparency by host','host_descriptions.jpg'],
}
for col in cols:
    p=tmp[[col,'number_of_reviews_ltm']].groupby(col).mean()
    inputs={
        'title':f'Impact due to prefernce for {props[col][0]}',
        'y_label':'Avg No.of Vists per year',
        'x_label':'Types of Listings',
        'kind':'bar',
        'figWidth':20,
        'figHeight':30,
        'labelsize':30,
        'fontsize':30,
        'legendsize':20,
        'legendlabel':'Visits',
        'xlabelrotation':45,
        'file_': f'results/{props[col][1]}',
    }
    plot_graph(list(map(lambda x : labels[col][x],p.index.values)),
                    p.values.flatten(),**inputs)

#results6 : seasonality check
import pandas as pd
from clean_data import clean_preprocess_reviews
reviews=clean_preprocess_reviews(reviews)
labels=['jan-2020','feb-2020','mar-2020','apr-2020','may-2020',
        'june-2020','jul-2020','aug-2020','sep-2020','oct-2020',
        'nov-2020','dec-2020']
bins=list(map(lambda x : pd.to_datetime(x),labels+['Jan-2021']))
tmp=reviews.groupby(pd.cut(
                    reviews['date'],
                    bins=bins,
                    labels=labels))['date'].count()
inputs={
        'title':'Visits variation across the year',
        'y_label':'No.of Vists per month',
        'x_label':'Months',
        'kind':'bar',
        'figWidth':10,
        'figHeight':10,
        'labelsize':5,
        'fontsize':10,
        'legendsize':5,
        'legendlabel':'Visits',
        'xlabelrotation':45,
        'file_': 'results/monthly_visits.jpg',
    }
plot_graph(list(tmp.index.values),
                    tmp.values.flatten(),**inputs)
    
#results7: Finding top 3 impact creating explanatory variables
from model_functions import model
from functions import subtract_elem
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