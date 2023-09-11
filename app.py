import json 
import pandas as pd 
import re
import numpy as np
import geopandas as gpd
from streamlit_folium import st_folium
import streamlit as st
import random 
import json 


schools = pd.read_csv('schools - schools.csv')
work_permissions = pd.read_csv('work_permissions.csv')


st.set_page_config(page_title='My Webpage', page_icon=':tada', layout='wide')

st.title("Welcome to CAA Chabely's CAA Map!!")
st.write("Hi I'm Chabely, a Certified Anesthesiologist Assistant! Check out my [Youtube](https://www.youtube.com/@CAALifestyle) for more information!!!")

st.markdown("---")
st.subheader("Updates: :tada: :tada: :tada:")
st.markdown("- Nevada 2024: Veterans Affairs ->> Full Practice")
st.markdown("---")
st.subheader('Certified Anesthesiologist Assistant Practice USA Map, Sep. 2023')

with open("output.html", "r") as f:
    html_content = f.read()

with st.container():
    st.components.v1.html(html_content, height=600)  


with st.container():
    c1,c2 = st.columns([2, 4])
    with c1:
        st.subheader('State Practice')
        st.dataframe(work_permissions)
    with c2:
        st.subheader('AA Programs')
        st.dataframe(schools.iloc[:,:-2])
