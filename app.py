from collections import namedtuple
import pandas as pd
from ydata_profiling import ProfileReport
import pandas as pd
import json
import time
import streamlit as st

from PIL import Image
import os


st.set_page_config(
    page_title="EmiProfile",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "mailto:overmars86@gmail.com"
    }
    
)

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

image = Image.open("Emicool_Logo.80kb_high_res-removebg-preview.png")
st.image(image)

"""
# Welcome to Emi Data Profiler!

This tool is for Emicool employees only.






"""

uploaded_file = st.file_uploader("Upload a csv file", type=['csv'])
if uploaded_file is not None:
    file = pd.read_csv(uploaded_file)
    with st.spinner('Generating the report for download...'):
        report = ProfileReport(file)
        report = report.to_html()
        donwload = st.download_button('Download', report, 'report.html')
        if donwload == True:
            uploaded_file.close()
            # st.write("Thank you, come again!")
    
                

                    


        
