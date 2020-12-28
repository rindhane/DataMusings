#! /usr/bin/env ipython
'''main file to execute the project'''


#downloading data into memory
from downloader import get_data
df_dict=get_data()
listings=df_dict['listings']
calendar=df_dict['calendar']
reviews=df_dict['reviews']

#cleaning & preprocessing the data
from clean_data import clean_preprocess_data
data=clean_preprocess_data(listings)


#plotting the results from the exploratory analysis

#results1 : Broad understanding of earning & avg.price


#results 2/ plot1:  various listings
from plot_functions import plot_graph
from plot_functions import range_without_outliers
inputs= {
    'kind' : 'hist',
    'bins' : 200,
    'x_label' : 'Listings Prices in Boston',
    'y_label': "No. of Vists/Annually", 
    'labelsize': 20,
    'fontsize' : 30,
    'xlim':range_without_outliers(data['price']),
    'legendlabel':'price vs demand',
    'legendsize':20,
    'file_': 'price_demand.jpg'
}

plot_graph(data['price'].values, **inputs)

#results3 : Variation of avg.price & 
from plot_functions import plot_graph_bar_line
tmp1=data[['neighbourhood_cleansed',
     'annual_earnings']].groupby(['neighbourhood_cleansed']).mean()
tmp2=data[['neighbourhood_cleansed',
     'price']].groupby(['neighbourhood_cleansed']).mean()
inputs={
    'title':'Annual Earning & Price/Night variation across Boston areas',
    'x_label':'avg. annual_earnings',
    'y_label':'Areas in Boston',
    'kind':'barh',
    'x_label2': 'avg.price/night',
    'figWidth':20,
    'figHeight':30,
    'labelsize':30,
    'fontsize':30,
    'legendsize':20,
    'legendlabel':'annual earning',
    'legendlabel2': 'price',
    'file_': 'earning_distribution.jpg'
    }
plot_graph_bar_line([tmp1.index.values,tmp1.values.flatten()],
          [tmp2.values.flatten(),tmp2.index.values,], 
           **inputs)