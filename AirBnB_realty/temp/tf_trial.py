%%time
import tensorflow as tf
from clean_data import clean_preprocess_listings
from downloader import get_data
import pandas as pd
import math 
df_dict=get_data()
listings=df_dict['listings']
data=clean_preprocess_listings(listings)
from functions import subtract_elem
model=tf.keras.models.Sequential([
  tf.keras.layers.Dense(2048,input_shape=(58,),activation= "relu", kernel_initializer='normal'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(512, activation= "relu", kernel_initializer='normal'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(64, activation= "relu", kernel_initializer='normal'),
  tf.keras.layers.Dense(1,)
])
model.compile(optimizer="adam",
              loss="mse",
              metrics=["mean_squared_error"])
tmp=pd.get_dummies(data,columns=['neighbourhood_cleansed','bathrooms_type',
                                'room_type'],
                            prefix=['neighbourhoods','bathroom','room_type'],
                            prefix_sep='-')
outcomes=['annual_earnings']
variables=subtract_elem(tmp.columns,outcomes)
n=len(tmp)
n_train=int(0.7*n)
X_train=tmp[variables].iloc[:n_train]
Y_train=tmp[outcomes].iloc[:n_train]
model.fit(X_train.values, Y_train.values, epochs=2000,verbose=0)
X_test=tmp[variables].iloc[n_train:]
Y_test=tmp[outcomes].iloc[n_train:]
results=model.evaluate(X_test.values,Y_test.values, verbose=1)
print('rms=', math.sqrt(results[0]))