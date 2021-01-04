#! /usr/bin/env ipython
'''main file to execute the project'''

#downloading data into memory
from datetime import datetime
from downloader import get_data
city = "Boston"
df_dict=get_data(city="Boston", 
                latest_by=datetime.today().strftime("%d-%B-%Y"))
listings=df_dict['listings']
calendar=df_dict['calendar']
reviews=df_dict['reviews']

#cleaning & preprocessing the data
from clean_data import clean_preprocess_listings
data=clean_preprocess_listings(listings)
#plotting the results from the exploratory analysis

#results1/plot1 : Broad understanding of earning & avg.price
from plot_functions import plot_graph
from functions import range_without_outliers
inputs= {
    'title':f'Annual earning across Airbnb listing in {city} ',
    'kind' : 'hist',
    'bins' : 600,
    'x_label' : f'Earning by a single listing',
    'y_label': "No. of Listing", 
    'labelsize': 20,
    'fontsize' : 30,
    'xlim':range_without_outliers(data['annual_earnings'][data['annual_earnings']!=0]),
    'legendlabel':'Earning ',
    'legendsize':20,
    'file_': 'results/average_earning.jpg',
}

plot_graph(data['annual_earnings'][data['annual_earnings']!=0].values, **inputs)
print(f"The average price/night for a visitor in {city} based on\
available listings is ",data['price'].mean()," in US-Dollars")

#results 1/ plot2:  various listings
from plot_functions import plot_graph
from functions import range_without_outliers
inputs= {
    'title': f'Price/Night offering across Listings in {city}',
    'kind' : 'hist',
    'bins' : 200,
    'x_label' : f"Listings's Price/Night ",
    'y_label': "No. of Listings", 
    'labelsize': 20,
    'fontsize' : 30,
    'xlim':range_without_outliers(data['price']),
    'legendlabel':'price/night',
    'legendsize':20,
    'file_': 'results/price_options.jpg'
}
plot_graph(data['price'].values, **inputs)
#results 2/ plot1:  Most opted price by visitors to the city.
def price_demand(df):
  ans=list()
  tmp=data[['price','number_of_reviews_ltm']].apply(
      lambda col: [col['price']]*int(col['number_of_reviews_ltm']),axis=1 )
  for i in tmp:
    ans.extend(i)
  return pd.Series(ans)
inputs= {
    'title': f'Price/Night opted by tourists to {city}',
    'kind' : 'hist',
    'bins' : 50,
    'x_label' : f"Listings's Price/Night ",
    'y_label': "No. of Visits", 
    'labelsize': 20,
    'fontsize' : 30,
    'xlim':[0,range_without_outliers(price_demand(data))[1]],
    'legendlabel':'Visits',
    'legendsize':20,
    'file_': 'results/price_demand.jpg'
}
plot_graph(price_demand(data).values, **inputs)
print('Price with highest demand =','$'+str(int(price_demand(data).mean())))

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

#quick peak in correlation among other variables
inputs={
    'file_' : 'results/heatmap.jpg'
}
from plot_functions import plot_variable_corelation
plot_variable_corelation(data.corr(),**inputs)

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
import pandas as pd
from plot_functions import plot_coeff
tmp=data.drop(columns=['annual_earnings'])
tmp=pd.get_dummies(tmp,columns=['neighbourhood_cleansed','bathrooms_type',
                                'room_type'],
                            prefix=['neighbourhoods','bathroom','room_type'],
                            prefix_sep='-')
outcomes=['number_of_reviews_ltm']
variables=subtract_elem(tmp.columns,outcomes)
model.set_inputs(data=tmp,
                outcomes=outcomes,
                variables=variables)
model.train()
#model trained & plotting results
ans=model.model.model.named_steps.regressor.coef_
ans=ans.ravel()
order=ans.argsort()[::-1]
tmp=pd.concat([pd.Series(tmp.columns[order]),
                pd.Series(ans[order])], 
                axis=1,).\
                    rename(columns={0:'features',1:'visit_influencer'})
inputs={
    'file_':'results/top3.jpg',
    'show': False,
   'x':'visit_influencer',  
   'y':'features',
    'scale' : ['visit_influencer'],
    'height':5*2.54,
}
plot_coeff(tmp,**inputs)