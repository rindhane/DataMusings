import pandas as pd
import math
from sklearn.model_selection import train_test_split
from functions import self_setup_class
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.ensemble import AdaBoostRegressor
from sklearn.svm import SVR
def pass_self(self):
    return self

class ml_model_setup(self_setup_class):
    def __init__(self,data,**kwargs):
        super().__init__(data=data,**kwargs)
        if not('preprocessor' in kwargs):
            self.preprocessor=pass_self
    def get_data(self):       
        if not(hasattr(self,'preprocessor')):
            raise RuntimeError('preprocessor not defined')
        else:
            return self.data.apply(self.preprocessor)
    def get_train_test_split(self,**inputs):
        if getattr(self,'random_state',None) :
            random_state=self.random_state
        else:
            random_state=inputs.get('random_state',42)
        test_size=inputs.get('test_size',0.3)
        (self.train_index, 
        self.test_index) = train_test_split(
                                        self.get_data().index,
                                        random_state=random_state,
                                        test_size=test_size)
        return (self.train_index, self.test_index)
    def train(self,**kwargs):
        train,test=self.get_train_test_split()
        self.model.train(self.get_data()[self.variables].loc[train].values,
                         self.get_data()[self.outcomes].loc[train].values.ravel(),
                            **kwargs)
        self.save()
        self.evaluate(train=train,test=test) 
    def save(self):
        self.predictor=self.model.save()
    def evaluate(self,**kwargs):
        scorer=kwargs.get('scorer', mean_squared_error)
        y_true=self.get_data().loc[self.test_index][self.outcomes].values.ravel()
        y_pred=self.predictor(
                self.get_data().loc[self.test_index][self.variables].values)
        print('test rms_error = ', math.sqrt(scorer(y_true,y_pred)))
        
class setup(ml_model_setup) :
    def __init__(self,**kwargs):
        if 'data' in kwargs:
            super().__init__(**kwargs)
        else:
            super().__init__(data=None,**kwargs)
    @classmethod
    def existing_setup(cls,instance):
        return cls(**instance.__dict__)

class sklearn_model(self_setup_class):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_setup(**kwargs)
    def model_setup(self,**inputs):
        self.train=self.model.fit
        self.predict=self.model.predict
    def save(self, **inputs):
        return self.predict

#need model comparator & comparison plotter
#need model tuner based on gridsearchCV
#method to save gridsearchcv params and build model
#need model saver to save serialized model

pipe = Pipeline([
    #('poly', PolynomialFeatures(degree=2)),
    ('scaler', StandardScaler()),
    ('regressor', SVR(kernel='linear',
                    C=100, epsilon=0.001, 
                    cache_size=1000, 
                    tol=1e-4)),
    ])
regressor = sklearn_model(model=pipe)
model=ml_model_setup(data=None, model=regressor)
