from sqlite3 import dbapi2
import CovidAPI as ca
import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import sqlite3
from sqlite3 import Connection
from pathlib import Path
pio.templates.default = "plotly"
dbPath = 'US_Covid.db'
db = sqlite3.connect('US_Covid.db')
c = db.cursor()
c.execute("""SELECT DISTINCT state
    FROM us_covid
    """)

states = c.fetchall()
stateAbrvs = []
for state in states:
    for stt in state:
        stateAbrvs.append(stt)
c.close()
db.close()


keyMetrics = ['positive','negative', 'hospitalizedCurrently','hospitalizedCumulative','death','hospitalized','positiveIncrease','negativeIncrease','total','deathIncrease','hospitalizedIncrease']

#! Deprecated. Dataset updates are handled separately 
#def data_retrieval():
#    """Utilizes CovidAPI.py to handle data requests to "covidtracking.com" and
#    for keeping the data file updated
#    """
#    data_request = ca.CovidAPI()
#    data_request.setDataPath("Georgia_Covid.json")
#    data_request.updateData("ga")

#@st.cache(ttl=60*60*12)
#def load_data(filepath):
def load_data(stateAbrv):
    """This function is for loading and formatting the data file, and 
    removing columns containing only 'NaN' or 0

    Args:
        filepath (string): File path to dataset

    Returns:
        Dataframe: Returns formatted Pandas dataframe
    """
    #data_retrieval()
    #data = pd.read_json(filepath) #replaced by sql statements
    #db = sqlite3.connect('US_Covid.db')
    #c = db.cursor()
    #dataQuery = "SELECT * FROM %s_covid" % (stateAbrv)
    #data = pd.read_sql_query("SELECT * FROM us_covid ",db)
    dataPath = get_connection(dbPath)

    data = pd.read_sql_query("SELECT * FROM {}_covid".format(stateAbrv), dataPath) 
    data['date'] = pd.to_datetime(data['date'], format="%Y%m%d")
    data = data.dropna(axis='columns', how='all')
    data = data.loc[:, (data != 0).any(axis=0)]

    #c.execute("""SELECT DISTINCT state
    #FROM us_covid
    #""")

    #states = c.fetchall()
    #stateAbrvs = []
    #for state in states:
     #   for st in state:
      #      stateAbrvs.append(st)

    return data
    
@st.cache(hash_funcs={Connection: id})    
def get_connection(path: str):
    return sqlite3.connect(path, check_same_thread=False)




#stateFrame = load_data("Georgia_Covid.json")
#stateFrame, stateAbrvs = load_data('US_Covid.db')

st.sidebar.header("Navigation")
sections = st.sidebar.selectbox("Go to",['Single State', 'State Comparison', 'Future Goals'])



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
                    label="Yearly",
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



if(sections == 'Single State'):
    stateSelect = st.sidebar.selectbox("Choose state",stateAbrvs,index=11)

    stateFrame = load_data(stateSelect)

    st.title('US Covid Statistics')
    st.write("This app is for visualizing United States Covid data")
    st.write("The data for this app was acquired from [The COVID Tracking Project](https://covidtracking.com/), where every day volunteers are ensuring that the public has the best available Covid data.")

    if st.checkbox("Show Data"):
        st.dataframe(stateFrame)
        st.write("Dataset contains %s columns and %s rows" % (len(stateFrame.columns),len(stateFrame)))
    

    try:
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
        pos_inc_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['positiveIncrease'],name='Positive Increase',text=stateFrame['positiveIncrease'],textposition='inside',))
        
        moving_avg_7 = stateFrame['positiveIncrease'].rolling(7).mean()
        pos_inc_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))
        pos_inc_fig.update_yaxes(automargin=True)
        
        st.plotly_chart(pos_inc_fig, use_container_width=False)
    except:
        st.markdown("**Insufficient positive increase data available**")

    if(st.checkbox("Total Positive")):
        try:
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
            pos_cumu_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['positive'],name='Positive',text=stateFrame['positive'],textposition='inside',))
        
            moving_avg_7 = stateFrame['positive'].rolling(7).mean()
            pos_cumu_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))

            pos_cumu_fig.update_yaxes(automargin=True)
        
            st.plotly_chart(pos_cumu_fig, use_container_width=False)
        except:
            st.markdown("**Insufficient hospitalization increase data available**")

    try:
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
        dth_inc_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['deathIncrease'],name='Death Increase',text=stateFrame['deathIncrease'],textposition='inside',))
        
        moving_avg_7 = stateFrame['deathIncrease'].rolling(7).mean()
        dth_inc_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))

        dth_inc_fig.update_yaxes(automargin=True)
        
        st.plotly_chart(dth_inc_fig, use_container_width=False)
    except:
        st.markdown("**Insufficient hospitalization increase data available**")

    
    # Selectbox Death Cumulative
    if(st.checkbox("Death Cumulative")):
        try:
            dth_cumu_fig = go.Figure()
            dth_cumu_fig.update_layout(covid_template)
            dth_cumu_fig.update_layout(
                title="Total Deaths",
                xaxis_title='Date',
                yaxis_title='Deaths Cumulative',
                legend_title="Legend",
                xaxis=slider_template
                )
            dth_cumu_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['death'],name='Death Count',text=stateFrame['death'],textposition='inside',))
        
            moving_avg_7 = stateFrame['death'].rolling(7).mean()
            dth_cumu_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))

            dth_cumu_fig.update_yaxes(automargin=True)
        
            st.plotly_chart(dth_cumu_fig, use_container_width=False)
        except:
            st.markdown("**Insufficient hospitalization increase data available**")
    try:
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
    
        hosp_inc_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['hospitalizedIncrease'],name='Hospitalized Increase',text=stateFrame['hospitalizedIncrease'],textposition='inside',))
    


        moving_avg_7 = stateFrame['hospitalizedIncrease'].rolling(7).mean()
        hosp_inc_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))

        hosp_inc_fig.update_yaxes(automargin=True)
    
        st.plotly_chart(hosp_inc_fig, use_container_width=False)
    except:
        st.markdown("**Insufficient hospitalization increase data available**")

    try:
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
        hosp_cur_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['hospitalizedCurrently'],name='Hosptialized Currently',text=stateFrame['hospitalizedCurrently'],textposition='inside',))
        
        moving_avg_7 = stateFrame['hospitalizedCurrently'].rolling(7).mean()
        hosp_cur_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))

        hosp_cur_fig.update_yaxes(automargin=True)
        
        st.plotly_chart(hosp_cur_fig, use_container_width=False)
    except:
        st.markdown("**Insufficient hospitalization increase data available**")

    
    # Selectbox Hospitalized Cumulative 
    if(st.checkbox("Hospitalized Cumulative")):
        try:
            hosp_cumu_fig = go.Figure()
            hosp_cumu_fig.update_layout(covid_template)
            hosp_cumu_fig.update_layout(
                title="Total Hospitalizations",
                xaxis_title='Date',
                yaxis_title='Hospitalized Cumulative',
                legend_title="Legend",
                xaxis=slider_template
                )
            hosp_cumu_fig.add_trace(go.Bar(x=stateFrame['date'],y=stateFrame['hospitalizedCumulative'],name='positive',text=stateFrame['hospitalizedCumulative'],textposition='inside',))
        
            moving_avg_7 = stateFrame['hospitalizedCumulative'].rolling(7).mean()
            hosp_cumu_fig.add_trace(go.Scatter(x=stateFrame['date'],y=moving_avg_7, name="7-Day average"))

            hosp_cumu_fig.update_yaxes(automargin=True)
        
            st.plotly_chart(hosp_cumu_fig, use_container_width=False)
        except:
            st.markdown("**Insufficient hospitalization increase data available**")

if(sections =='State Comparison'):
    st.title("State Comparison")
    firstStateSelect = st.sidebar.selectbox("Choose first state",stateAbrvs,index=11)
    secondStateSelect = st.sidebar.selectbox("Choose second state",stateAbrvs,index=10)
    #compareMetric = st.sidebar.selectbox("Comparison metric", )


    firstStateFrame = load_data(firstStateSelect)
    secondStateFrame = load_data(secondStateSelect)

    compareMetric = st.sidebar.selectbox("Comparison metric", keyMetrics,index=6)

    comp_fig = go.Figure()
    comp_fig.update_layout(covid_template)
    comp_fig.update_layout(
            title=compareMetric + " Comparison",
            xaxis_title='Date',
            yaxis_title=compareMetric,
            legend_title="Legend",
            xaxis=slider_template
            )
    
    comp_fig.add_trace(go.Bar(x=firstStateFrame['date'],y=firstStateFrame[compareMetric],name=firstStateSelect,text=firstStateFrame[compareMetric],textposition='inside',))
    comp_fig.add_trace(go.Bar(x=secondStateFrame['date'],y=secondStateFrame[compareMetric],name=secondStateSelect,text=secondStateFrame[compareMetric],textposition='inside',))
    


    moving_avg_7 = firstStateFrame[compareMetric].rolling(7).mean()
    moving_avg_72 = secondStateFrame[compareMetric].rolling(7).mean()

    comp_fig.add_trace(go.Scatter(x=firstStateFrame['date'],y=moving_avg_7, name=firstStateSelect + " 7-Day average"))
    comp_fig.add_trace(go.Scatter(x=secondStateFrame['date'],y=moving_avg_72, name=secondStateSelect + " 7-Day average"))


    #comp_fig.update_layout(barmode='stack')
    comp_fig.update_yaxes(automargin=True)

    st.plotly_chart(comp_fig, use_container_width=False)


if(sections == 'Future Goals'):
    st.title("Future Goals")
    st.markdown("<ul> <s><b><li>Add state selection</s> <b><li>Include national average comparisons within graphs <ul> ",unsafe_allow_html=True)

st.sidebar.header("About")
st.sidebar.info("This app is maintained by Matthew Bailey. The code can be found on [Github](https://github.com/MatthewBailey97/Georgia_Covid)")