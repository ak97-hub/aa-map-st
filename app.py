import pandas as pd 
from streamlit_folium import st_folium
import streamlit as st


schools = pd.read_csv('schools - schools.csv')
work_permissions = pd.read_csv('work_permissions.csv')


st.set_page_config(page_title='My Webpage', page_icon=':tada', layout='wide')

st.title("Welcome to CAA Chabely's CAA Map!!")
st.write("Hi I'm Chabely, a Certified Anesthesiologist Assistant! Check out my [Youtube](https://www.youtube.com/@CAALifestyle) for more information!!!")

st.markdown("---")
st.subheader("Updates: :tada: :tada: :tada:")
st.markdown("- University of Mary Hardin-Baylor Opening in Fall 2026")
st.markdown("- Tennessee Full Practice 2026")
st.markdown("- Virginia CAA state legislature- effective 7/1/25!!")
st.markdown("- Kansas City University announces plans for anesthesiologist assistant program beginning in January 2026")
st.markdown("- Washington 2024: Veterans Affairs ->> Full Practice")
st.markdown("- Nevada 2023: Veterans Affairs ->> Full Practice; bill signed 2023, effective 1/1/24")
st.subheader("NOTES:")
st.markdown("- Kentucky- requires PA licensing in addition to AA licensing")
st.markdown("- Click circle on map to see school name")

st.markdown("---")
st.subheader('Certified Anesthesiologist Assistant Practice USA Map, March 2025')

with open("updated_output.html", "r") as f:
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
