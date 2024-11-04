import json 
import pandas as pd 
import plotly.graph_objects as go 
import re
import numpy as np
import geopandas as gpd

with open("./gz_2010_us_040_00_500k.json") as response:
    geo = json.load(response)

schools = pd.read_csv('https://raw.githubusercontent.com/ak97-hub/aa-map-st/main/schools%20-%20schools.csv')
work_permissions = pd.read_csv('https://raw.githubusercontent.com/ak97-hub/aa-map-st/main/work_permissions.csv')

state_centroid_data = [("AK","66.588753","-152.493062","Alaska"),
("AL","32.318231","-86.902298","Alabama"),
("AR","35.20105","-91.831833","Arkansas"),
("AZ","34.048928","-111.093731","Arizona"),
("CA","36.778261","-119.417932","California"),
("CO","39.550051","-105.782067","Colorado"),
("CT","41.803221","-72.587749","Connecticut"),
("DC","38.905985","-77.033418","District of Columbia"),
("DE","38.910832","-75.52767","Delaware"),
("FL","27.664827","-81.515754","Florida"),
("GA","32.157435","-82.907123","Georgia"),
("HI","19.898682","-155.665857","Hawaii"),
("IA","41.878003","-93.097702","Iowa"),
("ID","44.068202","-114.742041","Idaho"),
("IL","40.633125","-89.398528","Illinois"),
("IN","40.551217","-85.602364","Indiana"),
("KS","39.011902","-98.484246","Kansas"),
("KY","37.839333","-84.270018","Kentucky"),
("LA","31.244823","-92.145024","Louisiana"),
("MA","42.407211","-71.882437","Massachusetts"),
("MD","39.045755","-76.641271","Maryland"),
("ME","45.253783","-69.445469","Maine"),
("MI","43.914844","-84.902364","Michigan"),
("MN","46.729553","-94.6859","Minnesota"),
("MO","37.964253","-91.831833","Missouri"),
("MS","32.354668","-89.398528","Mississippi"),
("MT","46.879682","-110.362566","Montana"),
("NC","35.759573","-79.0193","North Carolina"),
("ND","47.551493","-101.002012","North Dakota"),
("NE","41.492537","-99.901813","Nebraska"),
("NH","43.193852","-71.572395","New Hampshire"),
("NJ","40.058324","-74.405661","New Jersey"),
("NM","34.97273","-105.032363","New Mexico"),
("NV","38.80261","-116.419389","Nevada"),
("NY","43.299428","-75.217933","New York"),
("OH","40.417287","-82.907123","Ohio"),
("OK","35.007752","-97.092877","Oklahoma"),
("OR","43.804133","-120.554201","Oregon"),
("PA","41.203322","-77.194525","Pennsylvania"),
("PR","18.220833","-66.590149","Puerto Rico"),
("RI","41.580095","-71.477429","Rhode Island"),
("SC","33.836081","-81.163725","South Carolina"),
("SD","43.969515","-99.901813","South Dakota"),
("TN","35.517491","-86.580447","Tennessee"),
("TX","31.968599","-99.901813","Texas"),
("UT","39.32098","-111.093731","Utah"),
("VA","37.431573","-78.656894","Virginia"),
("VT","44.558803","-72.577841","Vermont"),
("WA","47.751074","-120.740139","Washington"),
("WI","43.78444","-88.787868","Wisconsin"),
("WV","38.597626","-80.454903","West Virginia"),
("WY","43.075968","-107.290284","Wyoming"),
]

state_centroids = pd.DataFrame(state_centroid_data,columns=["state","latitude","longitude","name"])

color_dict = {'Full Practice': '#88CED4',
              'Veteran Affairs': '#DCDDDC',
              'Delegatory': '#C2E5DD'}

color_dict2 = {'Summer':'#e1fc88',
               'Fall':'#f25235',
               'Spring':'#fc88c0', 
               'Unknown':'grey',
               np.nan: 'grey'}

# Read the Shapefile into a GeoDataFrame
gdf = gpd.read_file('./gz_2010_us_040_00_500k.json')
gdf = gdf.merge(work_permissions, left_on ='NAME', right_on='State')
gdf['fill'] = gdf.Practice.map(color_dict)

# Convert to Geo Json
geo = gdf.to_json()

import folium
import json

# Define circle marker parameters
circle_radius = 6  # Radius of the circle in meters
circle_color = None  # Color of the circle outline
circle_fill_color = 'yellow'  # Color to fill the circle

# Create a circle marker
def c_mark(marker_latitude, marker_longitude, label, circle_fill_color, circle_color, circle_radius):
    circle_marker = folium.CircleMarker(
        location=[marker_latitude, marker_longitude],
        radius=circle_radius,
        color=circle_color,
        fill=True,
        fill_color=circle_fill_color,
        fill_opacity=0.85,
        popup=label
    )
    return circle_marker


# Create a Folium Map object
m = folium.Map(location=[40, -96], zoom_start=4.4)


# Add the GeoJSON layer with fill color based on the "fill" property
folium.GeoJson(
    geo,
    name="geojson_layer",
    style_function=lambda feature: {
        "fillColor": feature["properties"]["fill"],  # Use the "fill" property for fillColor
        "color": "black",
        "weight": 0.2,
        'fillOpacity':0.8
    },
).add_to(m)


for idx, datarow in state_centroids.iterrows():
    label, coord = (datarow['state'], (datarow['latitude'], datarow['longitude']))
    folium.Marker(coord, icon=folium.DivIcon(html=f'<div style="font-size: 8px";>{label}</div>')).add_to(m)

for idx, school in schools.iterrows():
    label, coord = (school['School'], (school['lat'], school['lon']))
    start_term_color = color_dict2[school['Start Term']]
    #folium.Marker(coord, popup=label).add_to(m)
    circle = c_mark(label=label, 
                    circle_radius = 5,  # Radius of the circle in meters
                    circle_color = None,  # Color of the circle outline
                    circle_fill_color = start_term_color,  # Color to fill the circle
                    *coord)
    circle.add_to(m)

# Create a custom HTML legend
legend_html = """
<div style="position: fixed; top: 10px; right: 10px; background-color: white; border: 0.2px solid black; z-index: 1000; padding: 5px;">
    <div style="font-weight: bold; font-size: 14px; margin-bottom: 5px;">Practices</div> <!-- Title -->
    <!-- Legend 1 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: #88CED4; margin-right: 5px;"></div>
        <span style="font-size: 12px;">Full Practice</span>
    </div>
    <!-- Legend 2 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: #C2E5DD; margin-right: 5px;"></div>
        <span style="font-size: 12px;">Delegatory</span>
    </div>
     <!-- Legend 3 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: #DCDDDC; margin-right: 5px;"></div>
        <span style="font-size: 12px;">Veteran Affairs</span>
    </div>
</div>
"""

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

legend_html = f"""
<div style="position: fixed; top: 110px; right: 10px; background-color: white; border: 0.2px solid black; z-index: 1000; padding: 5px;">
    <div style="font-weight: bold; font-size: 14px; margin-bottom: 5px;">Schools-<br>Start Term</div> <!-- Title -->
    <!-- Legend 1 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: {color_dict2['Summer']}; margin-right: 5px; border-radius: 50%;"></div>
        <span style="font-size: 12px;">Summer</span>
    </div>
    <!-- Legend 2 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: {color_dict2['Fall']}; margin-right: 5px; border-radius: 50%;"></div>
        <span style="font-size: 12px;">Fall</span>
    </div>
     <!-- Legend 3 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: {color_dict2['Spring']}; margin-right: 5px; border-radius: 50%;"></div>
        <span style="font-size: 12px;">Spring</span>
    </div>
    <!-- Legend 3 -->
    <div style="display: flex; align-items: center; margin-bottom: 3px;">
        <div style="width: 16px; height: 16px; background-color: {color_dict2[np.nan]}; margin-right: 5px; border-radius: 50%;"></div>
        <span style="font-size: 12px;">Unknown</span>
    </div>
</div>
"""

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))
# Save the map to an HTML file

m.save('output.html')
m
