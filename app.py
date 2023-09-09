import streamlit as st
import plotly.express as px
import random 
import json 
import pandas as pd 
import plotly.graph_objects as go 
import re
coords = pd.read_csv('List_of_geographic_centers_of_the_United_States_2.csv')

def get_coords(x):
    input_string = x.split('/\ufeff')[0].split('/')[1]
    output_string = re.sub(r'[^0-9\s.]', '', input_string)
    _, lat, lon = output_string.split(' ')
    return pd.Series({'lat':lat, 'lon':lon})

coords.loc[:, ['lat','lon']] = coords.Coordinates.apply(get_coords)
coords.columns = ['State','Location','Coordinates','lat','lon']
coords.head(3)

with open("./gz_2010_us_040_00_500k.json") as response:
    geo = json.load(response)

schools = pd.read_csv('schools - schools.csv')
work_permissions = pd.read_csv('work_permissions.csv')


st.set_page_config(page_title='My Webpage', page_icon=':tada', layout='wide')

st.title("Welcome to CAA Chabely's CAA Map!!")
st.write("Hi I'm Chabely, a Certified Anesthesiologist Assistant! Check out my [Youtube](https://www.youtube.com/@CAALifestyle) for more information!!!")
fig = px.choropleth_mapbox(work_permissions, 
                           geojson=geo, 
                           locations='State',
                           color='Practice',
                           featureidkey="properties.NAME",
                           center={"lat": 40, "lon": -96.0},
                           mapbox_style="carto-positron", zoom=3, opacity=0.6,
                           color_discrete_sequence=['#88CED4', # Full practice
                                                    '#DCDDDC', # Vets
                                                    '#C2E5DD']) # Delegatory


fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
texttrace = go.Scattermapbox(
        lat=schools['lat'],
        lon=schools['lon'],
        text=schools['School'],
        fillcolor='grey',
        marker=dict(
        size=12,  # Adjust the size of the dots
        color='rgb(242, 177, 172)',  # Set the color to red
        opacity=0.85,
        #symbol='square' # Adjust the opacity of the dots
        ),
        name='schools',
        mode='markers'
    )

fig.add_trace(texttrace)
st.markdown("---")
st.subheader("Updates: :tada: :tada: :tada:")
st.markdown("- Nevada 2024: Veterans Affairs ->> Full Practice")
st.markdown("---")
st.subheader('Certified Anesthesiologist Assistant Practice USA Map, Sep. 2023')
st.plotly_chart(fig)

with st.container():
	c1,c2 = st.columns(2)
	with c1:
		st.subheader('State Practice')
		st.dataframe(work_permissions)
	with c2:
		st.subheader('AA Programs')
		st.dataframe(schools.iloc[:,:-2])
