"""
ElTrack - Elephant Tracking System
Developed by: Adithya G
Updated: April 2025
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import phonenumbers
import folium
import math
import random
from phonenumbers import geocoder as gc
from opencage.geocoder import OpenCageGeocode
import os
from datetime import datetime

# Initialize app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages

# Dictionary to store recent tracking history
tracking_history = {}

# Function to calculate distance
def calculate_distance(lat, lng, x, y):
    """Calculate the distance between two geographical points in kilometers"""
    p = [lat, lng]
    q = [lat+x, lng+y]
    distance = math.dist(p, q)
    return round(distance * 111.1, 2)  # Convert to km and round to 2 decimal places

# Establishing zones based on distance
def get_zone(distance):
    """Determine danger zone based on distance"""
    if distance < 2:
        return 'red'
    elif distance < 3.5:
        return 'yellow'
    else:
        return 'green'

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    zone = 'green'  # Default zone
    distance = 0
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if request.method == 'POST':
        try:
            # Get the LoRa ID from user
            lora_id = request.form['lora_id']
            
            # In a real application, we would use this ID to look up real GPS coordinates
            # For this prototype, we'll generate random coordinates in India
            
            # Base coordinates (somewhere in central India)
            base_lat = 22.3511148
            base_lng = 78.6677428
            
            # Generate random offset for elephant position (simulating real tracker data)
            ele_lat_offset = random.uniform(-0.05, 0.05)
            ele_lng_offset = random.uniform(-0.05, 0.05)
            
            # Elephant coordinates
            ele_lat = base_lat + ele_lat_offset
            ele_lng = base_lng + ele_lng_offset
            
            # Generate train position with some randomness
            train_lat_offset = random.uniform(-0.08, 0.08)
            train_lng_offset = random.uniform(-0.08, 0.08)
            
            # Create the map using folium according to coordinates
            my_map = folium.Map(location=[ele_lat, ele_lng], zoom_start=10, 
                               tiles="OpenStreetMap")
            
            # Add the icons for the elephant and the train
            elephant_icon = folium.features.CustomIcon("static/elephant.png", icon_size=(50, 50))
            train_icon = folium.features.CustomIcon("static/train.png", icon_size=(40, 40))
            
            # Calculate the distance between the elephant and the train
            distance = calculate_distance(ele_lat, ele_lng, train_lat_offset, train_lng_offset)
            zone = get_zone(distance)
            
            # Add the markers for the train and the elephant on the map
            folium.Marker(
                [ele_lat, ele_lng], 
                popup=f"Elephant ID: {lora_id}", 
                icon=elephant_icon
            ).add_to(my_map)
            
            folium.Marker(
                [ele_lat + train_lat_offset, ele_lng + train_lng_offset], 
                popup="Train", 
                icon=train_icon
            ).add_to(my_map)
            
            # Draw a line connecting the two points
            folium.PolyLine(
                locations=[[ele_lat, ele_lng], 
                          [ele_lat + train_lat_offset, ele_lng + train_lng_offset]],
                color='blue',
                weight=2,
                opacity=0.7,
                popup=f"Distance: {distance} km"
            ).add_to(my_map)
            
            # Add distance circle around elephant
            folium.Circle(
                radius=2000,  # 2km radius (red zone)
                location=[ele_lat, ele_lng],
                color='red',
                fill=True,
                fill_opacity=0.2
            ).add_to(my_map)
            
            folium.Circle(
                radius=3500,  # 3.5km radius (yellow zone)
                location=[ele_lat, ele_lng],
                color='yellow',
                fill=True,
                fill_opacity=0.1
            ).add_to(my_map)
            
            # Save the map to templates
            my_map.save("templates/map_view.html")
            
            # Store tracking history
            if lora_id in tracking_history:
                tracking_history[lora_id].append({
                    'timestamp': timestamp,
                    'distance': distance,
                    'zone': zone
                })
                # Keep only the last 5 records
                tracking_history[lora_id] = tracking_history[lora_id][-5:]
            else:
                tracking_history[lora_id] = [{
                    'timestamp': timestamp,
                    'distance': distance,
                    'zone': zone
                }]
            
            flash(f"Elephant tracking successful. Distance from train: {distance} km", "success")
            
        except Exception as e:
            flash(f"Error processing tracking data: {str(e)}", "danger")
            return render_template('home.html', zone='green', distance=0)
            
    return render_template('home.html', zone=zone, distance=distance, 
                          tracking_history=tracking_history)

# Route for map
@app.route('/map_view')
def map_view():
    return render_template('map_view.html')

# API route for getting latest tracking data
@app.route('/api/tracking_data/<lora_id>', methods=['GET'])
def get_tracking_data(lora_id):
    if lora_id in tracking_history:
        return jsonify(tracking_history[lora_id])
    return jsonify([])

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Flask app run
if __name__ == '__main__':
    app.run(debug=True)