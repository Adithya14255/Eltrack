"""
    Eltrack - prototype
    by - Adithya G
"""


from flask import Flask, render_template, request
import phonenumbers
import folium
import math
import random
from phonenumbers import geocoder as gc
from opencage.geocoder import OpenCageGeocode

# initiaizing app
app = Flask(__name__)


# function to calculate distance
def distance(lat,lng,x,y):
    p=[lat,lng]
    q=[lat+x,lng+y]
    distance = math.dist(p,q)
    return distance*111.1

# establishing zones based on distance
zone = {0:'red',1:'red',2:'yellow',3:'green',4:'green',5:'green'}

#home route
@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        
        #get the phone number from user
        phone_number = request.form['phone']
 
        #parse the phone number according to phonenumbers format
        num_object = phonenumbers.parse(phone_number) 

        #get the description for the number
        locate = gc.description_for_number(num_object,'en')
        
        #API key for opencage
        key = "35fe7e54863942898334ae1ccc9d1757"
        geocoder = OpenCageGeocode(key)
        
        #query for locating the phone numeber
        query = str(locate)

        #getting the location details
        result = geocoder.geocode(query)

        #extracting the latitude and longitude from the result
        lat  = result[0]['geometry']['lat']
        lng  = result[0]['geometry']['lng']

        #create the map using folium acc to coordinates
        myMap = folium.Map(location = [lat,lng],zoom_start=9)

        #adding the icons for the elephant and the train
        icon1 = folium.features.CustomIcon("static/train.png", icon_size=(70,70))
        icon2 = folium.features.CustomIcon("static/elephant.png", icon_size=(100,100))
        
        #using random to determine the location of the train 
        #this is done only as example, supposed to be retrived from real time train data
        x= random.randrange(-100,100,3)/3000
        y= random.randrange(-100,100,3)/3000
        
        #calculate the distance between the elephant and the train
        temp=distance(lat,lng,x,y)

        #add the markers for the train and the elephant in the map
        folium.Marker([lat+x,lng+y],popup = locate,icon=icon1).add_to(myMap)
        folium.Marker([lat,lng],popup = locate,icon=icon2).add_to(myMap)
        
        #save the map to templates
        myMap.save("templates/mylocation.html")
        
        #return data for zone and distance
        return render_template('home.html',zone=zone[int(temp)],distance=temp)
    return render_template('home.html')

#route for map
@app.route('/mylocation',methods=['GET', 'POST'])
def mylocation():
    return render_template('mylocation.html')

#Flask app run 
if __name__ == '__main__':
    app.run(debug=True)

