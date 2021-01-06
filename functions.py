#file contains those utility functions which are 
#required for analysis of data.
import numpy as np


def reverse_dict(dict_):
    '''helper functions to generate dictonary(dict) where 
    new keys are values from original dict and keys of original are
    values in generated dictionary '''
    ans=dict()
    for key in dict_:
        ans[dict_[key]]=key
    return ans

def category_from_encoding(item, inverted_dict):
    '''To get the text category back from the numeric encoding'''
    return inverted_dict.get(item,np.nan) # see if np.nan can be replaced with something else


def range_without_outliers(series):
    '''Selecting the range for plotting the results.
        Here most extreme outliers are discarded'''
    q1=series.quantile(.25)
    q3=series.quantile(.75)
    iqr=q3-q1
    return [q1,q3+2*iqr]

class self_setup_class : 
    '''helper class to setup class which can create attributes from 
    the passed key value pairs during initalization of instance'''
    def __init__(self,**kwargs):
        self.set_inputs(**kwargs)
    def set_inputs(self,**inputs):
        for key in inputs:
            setattr(self,key,inputs.get(key))

def subtract_elem(x,y):
    '''helper function to get disjoint elements among two list'''
    z=list(x)
    for elem in y :
        if elem in z:
            z.remove(elem)
        else:
            pass
    return z

def plot_scaler_abs(array):
    '''helper function to scale the results into a positive unitary scale '''
    min=array.min()
    max=array.max()
    return (array-min)*(1/(max-min))

def plot_scaler(array):
    '''helper function to scale the results into a unitary scale '''
    t=abs(array).sum()
    f=array/t
    return array/t*1/f.sum()