import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
import folium
import random
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

# Function to load data
import pandas as pd

# If a file is uploaded, read it directly
file_path = "C:/Users/Deshakthi Akalanka/Pictures/CW/Global_Superstore_Lite.csv"
#if file is not None:
   # df = pd.read_csv(file )
#else:
    #df = pd.read_csv(file_path)


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
    
# Download data
cl1, cl2 = st.columns((2))

with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region_sales = df.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(region_sales.style.background_gradient(cmap="Oranges"))
        csv = region_sales.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

# Hierarchical view of Sales

# Calculate cumulative sales
df['Total Sales'] = df.groupby(['Region', 'Category'])['Sales'].transform(pd.Series.cumsum)

# Define colors for different levels (optional)
colors = ['skyblue', 'lightgreen', 'lightyellow']

fig4 = go.Figure()

# Add bars for each level, starting from the bottom (Sub-Category)
for i, level in enumerate(reversed(['Sub-Category', 'Category', 'Region'])):
    fig4.add_trace(go.Bar(
        x=df[level],
        y=df['Sales'] if level == 'Sub-Category' else df['Total Sales'],
        name=level,
        marker_color=colors[i]
    ))

fig4.update_layout(
    title="Hierarchical View of Sales",
    xaxis_title="Categories",
    yaxis_title="Sales",
    barmode="stack"  # Stack bars to show hierarchy
)

st.plotly_chart(fig4, use_container_width=True)


def download_hierarchical_data():
    data_to_download = df[['Region', 'Category', 'Sub-Category', 'Sales', 'Total Sales']]
    csv = data_to_download.to_csv(index=False).encode('utf-8')
    st.download_button("Download Hierarchical Data", data=csv, file_name="Hierarchical_Sales.csv", mime="text/csv")

# Add download button and display the chart
st.button("View Data", on_click=download_hierarchical_data)
st.plotly_chart(fig4, use_container_width=True)


# Segment wise Sales
chart1, chart2 = st.columns((2))

# Segment wise Sales
chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(df, values="Sales", names="Segment", template="plotly_dark")
    fig.update_traces(text=df["Segment"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(df, values="Sales", names="Category", template="gridon")
    fig.update_traces(text=df["Category"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
    
# Time Series Analysis
df["month_year"] = df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')
linechart = pd.DataFrame(df.groupby(df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="Sales", labels={"Sales": "Amount"}, height=500, width=1000,
               template="gridon")
st.plotly_chart(fig2, use_container_width=True)
with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')

    
# Histogram
st.subheader("Relationship between Sales and Profits")

# Create a histogram with a custom color scale
fig = px.histogram(df, x="Sales", title="Histogram of Sales")
fig2 = px.histogram(df, x="Profit", title="Histogram of Profits")
st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True
)
# Create histograms with download buttons
col1, col2 = st.columns(2)

with col1:
  fig = px.histogram(df, x="Sales", title="Histogram of Sales")
  st.plotly_chart(fig, use_container_width=True)
  st.button("View Data", on_click=download_sales_data)

with col2:
  fig2 = px.histogram(df, x="Profit", title="Histogram of Profits")
  st.plotly_chart(fig2, use_container_width=True)
  st.button("View Data", on_click=download_profit_data)

                
# Month wise Sub-Category Sales Summary
st.subheader("Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
    st.write(df_sample)

    st.markdown("Month wise sub-Category Table")
    df["month"] = df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data=df, values="Sales", index=["Sub-Category"], columns="month")
    st.write(sub_category_Year.style.background_gradient(cmap="Greens"))


# Download original DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")
                
                
                
                
chart1, chart2 = st.columns(2)

# Segment wise Sales
with chart1:
  st.subheader('Segment wise Sales')
  fig = px.pie(df, values="Sales", names="Segment", template="plotly_dark")
  fig.update_traces(text=df["Segment"], textposition="inside")
  st.plotly_chart(fig, use_container_width=True)

  # Download button for Segment wise Sales
  def download_segment_data():
    """
    Downloads the data used for the Segment wise Sales pie chart as a CSV file.
    """
    data_to_download = df[['Segment', 'Sales']]
    csv = data_to_download.to_csv(index=False).encode('utf-8')
    st.download_button("Download Segment Data", data=csv, file_name="Segment_Sales.csv", mime="text/csv")
  st.button("View Segment Data", on_click=download_segment_data)

# Category wise Sales
with chart2:
  st.subheader('Category wise Sales')
  fig = px.pie(df, values="Sales", names="Category", template="gridon")
  fig.update_traces(text=df["Category"], textposition="inside")
  st.plotly_chart(fig, use_container_width=True)

  # Download button for Category wise Sales
  def download_category_data():
    """
    Downloads the data used for the Category wise Sales pie chart as a CSV file.
    """
    data_to_download = df[['Category', 'Sales']]
    csv = data_to_download.to_csv(index=False).encode('utf-8')
    st.download_button("Download Category Data", data=csv, file_name="Category_Sales.csv", mime="text/csv")
  st.button("View Category Data", on_click=download_category_data)

