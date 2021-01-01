import pandas as pd
import math
from sklearn.model_selection import train_test_split
from functions import self_setup_class
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.ensemble import AdaBoostRegressor
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
        self.train_test_index=dict()
        (self.train_test_index['train'], 
        self.train_test_index['test']) = train_test_split(
                                        inputs.get('data').index,
                                        random_state=random_state,
                                        test_size=test_size)
        return inputs.get('data').loc[self.train_test_index[inputs.get('kind')]]
    def train(self,**kwargs):
        tmp=self.get_train_test_split(data=self.get_data(),kind='train')
        y=tmp[self.outcomes]
        self.model.train(tmp[self.variables],tmp[self.outcomes],**kwargs)
        self.evaluate(y_true=self.get_data().loc[self.train_test_index['test']][self.outcomes],
                    y_pred=self.model.predict(
                    self.get_data().loc[self.train_test_index['test']][self.variables]),)
        self.save()
    def save(self):
        self.predictor=self.model.save()
    def evaluate(self,**kwargs):
        print('rms_error = ', math.sqrt(mean_squared_error(kwargs['y_true'],kwargs['y_pred'])))
        
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

pipe1 = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('scaler', MinMaxScaler()),
    ('regressor', Lasso(alpha=0.0001,
                            tol=0.01,)),
    ])
regressor = sklearn_model(model=pipe1)
model=ml_model_setup(data=None, model=regressor)



