# Importing LIBRARIES

import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

# from pandas.io.json import json_normalize
from pandas import json_normalize # tranform JSON file into a pandas dataframe

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print('Libraries Imported')

# import csv file
status = pd.read_csv('primary_schools_2019_updated_w_totalpop.csv')

# status. csv file contains features variables such as Latitude, Longitude, Place, Region, SchoolName with Weather Parameters
status.drop(status.columns[[0]], axis=1, inplace=True)

def app():
    
    st.dataframe(status) # display dataframe
       
    
    
    # map = st.empty() # useful to overwrite a variable multiple times
    
    st.sidebar.header('Select a Location: ') # Adding a sidebar with select boxes    
    
    region = st.sidebar.selectbox('Select Region', 
                                  tuple(sorted(set(list(status['WARD'])))), # values to given as a tuple or simply within parenthesis
                                  index=None, # ordering
                                  placeholder="Select Ward") #default value in select box
    fig = st.empty()

    if region: # conditions gets valid when variable is initialized 
        region_data = status.loc[status['WARD'] == region]
        print(region_data.head())
        fig = px.scatter_mapbox(region_data, lat = "LATITUDE", lon = "LONGITUDE", hover_name="SCHOOL_NAM", hover_data = ["WARD", "REGION", "COUNCIL", "OWNERSHIP"],
                                color_discrete_sequence = ["fuchsia"], zoom = 10, height = 700, size = region_data["TOTAL_POPULATION"])
        
    else: # when no ward is selected, map of Tanzania and schools are presented
        fig = px.scatter_mapbox(status, lat = "LATITUDE", lon = "LONGITUDE", hover_name="SCHOOL_NAM", hover_data = ["WARD", "REGION", "COUNCIL", "OWNERSHIP"],
                                color_discrete_sequence = ["blue"], zoom = 5, height = 700, size = status["TOTAL_POPULATION"])

    
    # change background to raster tile map
    fig.update_layout( 
        mapbox_style="white-bg",
        mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "CycloSM",
            "source": [
                "https://a.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"
            ]
        }
        ])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # add plotly chart to streamlit
    st.plotly_chart(fig)
  
app()
