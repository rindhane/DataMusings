#file contains those utility functions which are 
#required for analysis of data.
import numpy as np


def reverse_dict(dict_):
    ans=dict()
    for key in dict_:
        ans[dict_[key]]=key
    return ans

def category_from_encoding(item, inverted_dict):
    return inverted_dict.get(item,np.nan) # see if np.nan can be replaced with something else

def price_demand(df):
  ans=list()
  tmp=data[['price','number_of_reviews_ltm']].apply(
      lambda col: [col['price']]*int(col['number_of_reviews_ltm']),axis=1 )
  for i in tmp:
    ans.extend(i)
  return pd.Series(ans)

def range_without_outliers(series):
    q1=series.quantile(.25)
    q3=series.quantile(.75)
    iqr=q3-q1
    return [q1,q3+2*iqr]

class self_setup_class : 
    def __init__(self,**kwargs):
        self.set_inputs(**kwargs)
    def set_inputs(self,**inputs):
        for key in inputs:
            setattr(self,key,inputs.get(key))

def subtract_elem(x,y):
    z=list(x)
    for elem in y :
        if elem in z:
            z.remove(elem)
        else:
            pass
    return z