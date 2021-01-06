#file contains functions to get cleaned data

#import statements
import pandas as pd 
import numpy as np
import json


def replace_nothing (item):
  return item

def replace_na(item):
  if pd.isna(item):
    return 0
  else : 
    return item

def replace_strings(item):
  if type(item)==str:
    return 1
  elif pd.isna(item):
    return 0
  else :
    return item

def get_rates(item):
  '''strings to float data type'''
  if type(item)==str:
      return float(item.replace('%',''))/100
  elif pd.isna(item):
      return 0

def categorical_values_rooms(item,get_encoding=False):
  '''function to encode the room_type into numeric categories'''
  vals = {  'Shared room': 1,
   'Private room':2, 
   'Entire home/apt':3, 
   'Hotel room': 4 ,}
  if get_encoding:
    return vals
  return vals.get(item,0)

def process_bath_text(item):
  '''function to encode the bath column into numeric categories'''
  ans=list()
  if pd.isna(item):
    ans.append(0)
    ans.append(0)
    return ans
  else : 
    item = item.lower()
    items=item.split(' ')
    if type(items[0])==str:
      ans.append(0)
    else :
      ans.append(int(items[0]))
    typeBath = "shared" if 'shared' in item else "private"
    ans.append(typeBath)
    return ans

def get_price(item):
  '''string to float data type'''
  return float(item.replace('$','').replace(',',''))

def ordinal_categories(item,cat_dict):
  '''helper function to convert cateogrial columns into 
  numeric categories based on the encoding in cat_dict  '''
  if item in cat_dict:
      return cat_dict[item]
  elif pd.isna(item):
      return 0
  else :
      return item

def get_json_list(item):
  '''to convert string characters list to python list'''
  if pd.isna(item):
      return 0
  else :
      return len(json.loads(item.replace('\'','\"')))

def process(col,string_numeric,process_dict):
  '''following function applies encoding rule to each of the respective column'''
  if col.name in process_dict :
      tmp=process_dict[col.name]
      return col.apply(tmp[0],**(tmp[1] if tmp[1:] else {}) )
  elif col.name in string_numeric:
      return col.apply(replace_strings)
  else:
      return col.apply(replace_na)

def combine(df,col_list, names):
    '''combine multiple columns  values into one column 
    and returns the resultant dataframe''' 
    for idx,cols in enumerate(col_list):
        tmp=pd.DataFrame(df[cols].apply(sum,axis=1),columns=names[idx])
        df=df.drop(columns=cols)
        df=pd.concat([df,tmp],axis=1)
    return df

def expand(cols,col_list,names_list):
  '''expand value in single columns  values into new columns 
    and returns the resultant dataframe'''
  for idx,col in enumerate(col_list):
    tmp=pd.Series(cols[col],index=names_list[idx])  
    cols=cols.drop(labels=[col])
    cols=cols.append(tmp,verify_integrity=True)
    return cols

def estimate_annual_earning(df):
  '''Helper function to genrate new column for annual earnings'''
  return df[['price','minimum_nights','number_of_reviews_ltm']].product(axis=1)

def clean_preprocess_listings(df):
    '''function to clean and preprocess the listings dataframe 
    and make it ready for further analysis'''
    listing_qualitative_factors=['name','description','neighborhood_overview','picture_url']
    listing_characterisitics=['neighbourhood_cleansed','room_type',
                          'accommodates','bathrooms_text','bedrooms',
                          'beds','amenities','minimum_nights']
    earning_estimators=['price','number_of_reviews_ltm']
    earning_influencers=['review_scores_rating', 'review_scores_accuracy',
        'review_scores_cleanliness', 'review_scores_checkin',
        'review_scores_communication', 'review_scores_location',
        'review_scores_value','license','instant_bookable' ]
    host_details = ['host_url', 'host_name','host_since',
              'host_location','host_about','host_thumbnail_url',
              'host_picture_url','host_neighbourhood',
              'host_has_profile_pic','host_total_listings_count']
    host_performance_parameters= ['host_response_time',
                                    'host_response_rate',
                                    'host_acceptance_rate',
                                    'host_verifications',
                                    'host_identity_verified',
                                    'host_is_superhost']
    process_dict = {
        'host_response_time' : [ordinal_categories, {'cat_dict':{'within a day' : 24,  
                                                    'within a few hours': 8, 
                                                    'within an hour': 1 ,
                                                    'a few days or more': 24*3}}],
        'host_acceptance_rate' : [get_rates],
        'host_response_rate' : [get_rates],
        'host_verifications' : [get_json_list],
        'host_acceptance_rate':[get_rates],
        'host_identity_verified' : [ordinal_categories, {'cat_dict':{'t':1, 'f' : 0}}], 
        'host_is_superhost': [ordinal_categories, {'cat_dict':{'t':1, 'f' : 0}}],
        'price' : [get_price],
        'instant_bookable': [ordinal_categories,{'cat_dict':{'t':1, 'f' : 0}}],
        'room_type': [categorical_values_rooms],
        'bathrooms_text':[process_bath_text],
        'amenities' : [get_json_list] ,
        }
    text_to_numeric = host_details[:-1]+\
                        listing_qualitative_factors+\
                        ['license']
    #drop the following columns
    #drop_column=discarded1
    #df=df.drop(columns=drop_column)
    cols_keep=listing_qualitative_factors+\
              listing_characterisitics+\
              earning_estimators+\
              earning_influencers+\
              host_details+\
              host_performance_parameters    
    df=df[cols_keep]
    df=df.apply(process, **{'string_numeric' : text_to_numeric,
                          'process_dict':process_dict})
    df=combine(df,
                [host_details[:-1],listing_qualitative_factors],
                names=[['host_descriptions'],['listing_descriptions']])
    df=df.apply(expand,axis=1,
                **{'col_list':['bathrooms_text'],
                'names_list':[['bathrooms_n','bathrooms_type'],],})
    df=df[df['price']!=0]
    df=df.assign(annual_earnings=estimate_annual_earning)
    return df    


'''keeping track of discarded columns'''
cols_discarded=['neighbourhood_group_cleansed', 'bathrooms','calendar_updated']+\
['reviews_per_month','latitude','longitude']+\
['neighbourhood','property_type']+\
['has_availability','availability_30','availability_60','availability_90','availability_365']+\
['maximum_nights','minimum_minimum_nights','maximum_minimum_nights',
'minimum_maximum_nights','maximum_maximum_nights','minimum_nights_avg_ntm',
'maximum_nights_avg_ntm']+\
['host_listings_count','host_id']+\
['number_of_reviews'] +\
['number_of_reviews_l30d'] +\
['calculated_host_listings_count',
        'calculated_host_listings_count_entire_homes',
        'calculated_host_listings_count_private_rooms',
        'calculated_host_listings_count_shared_rooms',]+\
['id','listing_url', 'scrape_id', 'last_scraped','calendar_last_scraped',
                      'first_review','last_review',]


def clean_preprocess_reviews(df):
  '''this function clean and preprocess the reviews dataframe'''
  process_dict= {
    'date':[pd.to_datetime,]
  }
  df=df.apply(process, **{'string_numeric' : [],
                          'process_dict':process_dict})
  df=df[df['date'] > pd.to_datetime('2020')]
  return df