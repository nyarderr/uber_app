import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

st.set_page_config(layout='centered')
st.title("Uber Pickups in NYC")

DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'

@st.cache_data
def load_data(nrows):
    df = pd.read_csv(DATA_URL, nrows=nrows)
    df.columns = [col.lower() for col in df.columns]
    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
    return df

col1,col2,col3 = st.columns(3)

nrows = col1.number_input("How many rows to load?",min_value=0,max_value=1028136)

c1,c2,c3,c4 = st.columns(4)

if c1.button("Load Data"):
    progress_placeholder = st.empty()
    progress_bar = progress_placeholder.progress(0)
    status = st.empty()
    for percent in range(0,101,10):
        if nrows <= 1000:
            time.sleep(0.001)
        else:
            time.sleep(0.1)
        progress_bar.progress(percent)
        status.text(f'Initializing..{percent}%')
    #load dataset
    df = load_data(nrows=nrows)
    st.session_state.df = df
    status.success('Data loaded successfully')
    progress_bar.empty()
    status.empty()
    
if st.session_state.get("df") is not None:
    if c2.checkbox("Show Raw Data", key='view'):
            st.subheader('Raw Data')
            st.write(st.session_state.df)

if st.session_state.get("df") is not None:
    #data for histogram
    df = st.session_state.df
    hour_to_filter = st.slider("hour",1,23,10, key='slider')
    hist_df = pd.DataFrame(df['date/time'].dt.hour.value_counts()).reset_index()
    plt = px.histogram(hist_df,x='date/time', y='count', template='simple_white', nbins=24, marginal='box',
    height=600) #hover_data=hist_df.columns)
    t1,t2 = st.tabs(["Histogram","Map"])
    
    with t1:
        st.plotly_chart(plt, theme='streamlit')
    #plot map data
    with t2:
        new_df = st.session_state.df.copy()
        new_df['hour']=new_df['date/time'].dt.hour
        map = px.scatter_map(new_df,lat='lat',lon='lon',color='hour', 
        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10, height=600)
        st.plotly_chart(map, theme='streamlit', container_width=False)
        #st.map(st.session_state.df[st.session_state.df['date/time'].dt.hour==hour_to_filter])


#st.session_state


