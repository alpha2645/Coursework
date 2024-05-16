import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
import folium
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

# Function to load data
def load_data(file):
    if file is not None:
        ld = pd.read_excel(file)
    else:
        #os.chdir(r"C:\Users\Deshakthi Akalanka\Pictures\CW")  
        ld = pd.read_excel("Global Superstore lite.xlsx")
    return ld

# Set page configuration
st.set_page_config(page_title="Superstore Dashboard", page_icon=":bar_chart:", layout="wide")

# Streamlit dashboard code
st.title("Superstore Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load data
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
df = load_data(fl)

# Filter by date
col1, col2 = st.columns((2))
with col1:
    st.subheader("Filter by Date")
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
    df["Order Date"] = pd.to_datetime(df["Order Date"]) 
    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()


# Sidebar filters
st.sidebar.header("Choose your filter: ")
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
state = st.sidebar.multiselect("Pick the State", df["State"].unique())
city = st.sidebar.multiselect("Pick the City", df["City"].unique())

if region:
    df = df[df["Region"].isin(region)]
if state:
    df = df[df["State"].isin(state)]
if city:
    df = df[df["City"].isin(city)]

category_df = df.groupby(by="Category", as_index=False)["Sales"].sum()

# Region wise sales
with col1:
    st.subheader("Region wise Sales")
    fig = px.bar(df, x="Region", y="Sales", color="Region", template="plotly_dark")
    fig.update_traces(textposition="outside")  
    st.plotly_chart(fig, use_container_width=True)
    
#Category wise sales
with col2:
    st.subheader("Category wise Sales")
    fig = px.pie(category_df, values="Sales", names="Category",
                 hole=0.4, labels={'Sales': 'Total Sales'})
    st.plotly_chart(fig, use_container_width=True, height=300)

