import tensorflow as tf
import pandas as pd
import numpy as np



data = pd.read_csv('Crop_recommendation.csv')
clases=data['label'].unique()

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

#using the same normalization used while training model
x=sc.fit_transform(data.drop('label', axis=1))

model = tf.keras.models.load_model('final.h5')
