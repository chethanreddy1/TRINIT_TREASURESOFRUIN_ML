import requests as rst
import numpy as np

#provides the crop names for input of predicted one hot encoded array
def onehottoclass(on,clases):
    cla=''
    for i in range(len(on)):
        if on[i]>0.5:
            cla=cla+', '+clases[i]

    return cla

#getting weather data for next 140 days from location provided by phone
def weather_fetch(lat,long):

    api_key = "ec91048bd3984a0ca6c13126231102"
    base_url = "http://api.weatherapi.com/v1/future.json?"
    dates=[f'2023-{3+int((13+i*14)/30):02d}-{(13+i*14)%30:02d}' for i in range(10)]
    temp,hum,precp=0,0,0
    #averaging values of every 14days for 10 times
    for date in dates:
        complete_url = base_url + "key=" + api_key + "&q=" + lat+', '+long+'&dt='+date
        response = rst.get(complete_url)
        x = response.json()
        temperature = x['forecast']['forecastday'][0]['day']['avgtemp_c']
        humidity = x['forecast']['forecastday'][0]['day']['avghumidity']
        precipitation=x['forecast']['forecastday'][0]['day']['totalprecip_mm']
        temp,hum,precp=temp+temperature, hum+humidity,precp+precipitation
    #getting district name from location coordinates
    city=x['location']['name']
    return temp/10,hum/10,precp/10,city

#gets features to input from message from app
def getfeatures(str):
    sp=str.split('/')[2:]
    temp,hum,precp,city=weather_fetch(sp[3],sp[4])
    sp=list(map(float,sp))
    ph=sp[-1]
    return sp[:3]+[temp]+[hum]+[ph]+[precp],city
    


