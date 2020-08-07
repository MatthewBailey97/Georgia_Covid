import CovidAPI as ca
import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates.default = "plotly"

def data_retrieval():
    """Utilizes CovidAPI.py to handle data requests to "covidtracking.com" and
    for keeping the data file updated
    """
    data_request = ca.CovidAPI()
    data_request.setDataPath("Georgia_Covid.json")
    data_request.updateData("ga")
    
@st.cache(ttl=60*60*12)
def load_data(filepath):
    """This function is for loading and formatting the data file, and 
    removing columns containing only 'NaN' or 0

    Args:
        filepath (string): File path to dataset

    Returns:
        Dataframe: Returns formatted Pandas dataframe
    """
    data_retrieval()
    data = pd.read_json(filepath)
    data['date'] = pd.to_datetime(data['date'], format="%Y%m%d")
    data = data.dropna(axis='columns', how='all')
    data = data.loc[:, (data != 0).any(axis=0)]
    return data

covid_data = load_data("Georgia_Covid.json")
st.sidebar.header("Navigation")
sections = st.sidebar.selectbox("Go to",['Home', 'Future Goals'])
st.sidebar.header("About")
st.sidebar.info("This app is maintained by Matthew Bailey. The code can be found on [Github](https://github.com/MatthewBailey97/Georgia_Covid)")


# Template for plot visuals
covid_template = dict(
    font=dict(
        #family="Courier New, monospace",
        size=15,
        color="Black"
    ),
    height=600,
    width=900,

    )

# Template for handling slider functionality for plots and providing buttons to alter time-period range of data
slider_template = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7.5,
                    label="Weekly",
                    step="day",
                    stepmode="todate"),
                dict(count=14,
                    label="Biweekly",
                    step="day",
                    stepmode="backward"),
                dict(count=1,
                    label="Monthly",
                    step="month",
                    stepmode="backward"),
                dict(count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"),
                dict(label="All",step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )

if(sections == 'Home'):

    st.title('Georgia Covid Statistics')
    st.write("This app is for visualizing Georgia's Covid data")
    st.write("The data for this app was acquired from [The COVID Tracking Project](https://covidtracking.com/), where every day volunteers are ensuring that the public has the best available Covid data.")

    if st.checkbox("Show Data"):
        st.dataframe(covid_data)
        st.write("Dataset contains %s columns and %s rows" % (len(covid_data.columns),len(covid_data)))

    # Positive increase
    pos_inc_fig = go.Figure()
    pos_inc_fig.update_layout(covid_template)
    pos_inc_fig.update_layout(
        #template=covid_template,
        title="Daily increase of positive cases",
        xaxis_title='Date',
        yaxis_title='Daily Positive Increase',
        legend_title="Legend",
        xaxis=slider_template
        )
    pos_inc_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positiveIncrease'],name='Positive Increase',text=covid_data['positiveIncrease'],textposition='inside',))
    
    moving_avg_7 = covid_data['positiveIncrease'].rolling(7).mean()
    pos_inc_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))
    pos_inc_fig.update_yaxes(automargin=True)
    
    st.plotly_chart(pos_inc_fig, use_container_width=False)


    if(st.checkbox("Total Positive")):
        # Total Positive
        pos_cumu_fig = go.Figure()
        pos_cumu_fig.update_layout(covid_template)
        pos_cumu_fig.update_layout(
            #template=covid_template,
            title="Total Positive Cases",
            xaxis_title='Date',
            yaxis_title='Positive Cumulative',
            legend_title="Legend",
            xaxis=slider_template
            )
        pos_cumu_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positive'],name='Positive',text=covid_data['positive'],textposition='inside',))
    
        moving_avg_7 = covid_data['positive'].rolling(7).mean()
        pos_cumu_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

        pos_cumu_fig.update_yaxes(automargin=True)
    
        st.plotly_chart(pos_cumu_fig, use_container_width=False)

    # Death Increase
    dth_inc_fig = go.Figure()
    dth_inc_fig.update_layout(covid_template)
    dth_inc_fig.update_layout(
        title="Daily Increase of Deaths",
        xaxis_title='Date',
        yaxis_title='Death Increase',
        legend_title="Legend",
        xaxis=slider_template
        )
    dth_inc_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['deathIncrease'],name='Death Increase',text=covid_data['deathIncrease'],textposition='inside',))
    
    moving_avg_7 = covid_data['deathIncrease'].rolling(7).mean()
    dth_inc_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

    dth_inc_fig.update_yaxes(automargin=True)
    
    st.plotly_chart(dth_inc_fig, use_container_width=False)
    # Selectbox Death Cumulative
    if(st.checkbox("Death Cumulative")):
        dth_cumu_fig = go.Figure()
        dth_cumu_fig.update_layout(covid_template)
        dth_cumu_fig.update_layout(
            title="Total Deaths",
            xaxis_title='Date',
            yaxis_title='Deaths Cumulative',
            legend_title="Legend",
            xaxis=slider_template
            )
        dth_cumu_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['death'],name='Death Count',text=covid_data['death'],textposition='inside',))
    
        moving_avg_7 = covid_data['death'].rolling(7).mean()
        dth_cumu_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

        dth_cumu_fig.update_yaxes(automargin=True)
    
        st.plotly_chart(dth_cumu_fig, use_container_width=False)

    # Hospitalized Increase
    hosp_inc_fig = go.Figure()
    hosp_inc_fig.update_layout(covid_template)
    hosp_inc_fig.update_layout(
        title="Daily Increase of Hospitalizations",
        xaxis_title='Date',
        yaxis_title='Hospitalization Increase',
        legend_title="Legend",
        xaxis=slider_template
        )
    hosp_inc_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['hospitalizedIncrease'],name='Hospitalized Increase',text=covid_data['hospitalizedIncrease'],textposition='inside',))
    
    moving_avg_7 = covid_data['hospitalizedIncrease'].rolling(7).mean()
    hosp_inc_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

    hosp_inc_fig.update_yaxes(automargin=True)
    
    st.plotly_chart(hosp_inc_fig, use_container_width=False)

    # Hospitalized Currently
    hosp_cur_fig = go.Figure()
    hosp_cur_fig.update_layout(covid_template)
    hosp_cur_fig.update_layout(
        title="Currently Hospitalized",
        xaxis_title='Date',
        yaxis_title='Hospitalized',
        legend_title="Legend",
        xaxis=slider_template
        )
    hosp_cur_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['hospitalizedCurrently'],name='Hosptialized Currently',text=covid_data['hospitalizedCurrently'],textposition='inside',))
    
    moving_avg_7 = covid_data['hospitalizedCurrently'].rolling(7).mean()
    hosp_cur_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

    hosp_cur_fig.update_yaxes(automargin=True)
    
    st.plotly_chart(hosp_cur_fig, use_container_width=False)

    # Selectbox Hospitalized Cumulative 
    if(st.checkbox("Hospitalized Cumulative")):
        hosp_cumu_fig = go.Figure()
        hosp_cumu_fig.update_layout(covid_template)
        hosp_cumu_fig.update_layout(
            title="Total Hospitalizations",
            xaxis_title='Date',
            yaxis_title='Hospitalized Cumulative',
            legend_title="Legend",
            xaxis=slider_template
            )
        hosp_cumu_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['hospitalizedCumulative'],name='positive',text=covid_data['hospitalizedCumulative'],textposition='inside',))
    
        moving_avg_7 = covid_data['hospitalizedCumulative'].rolling(7).mean()
        hosp_cumu_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

        hosp_cumu_fig.update_yaxes(automargin=True)
    
        st.plotly_chart(hosp_cumu_fig, use_container_width=False)

if(sections == 'Future Goals'):
    st.title("Future Goals")
    st.markdown("<ul><b><li>Add state selection <li>Include national average comparisons within graphs <ul> ",unsafe_allow_html=True)