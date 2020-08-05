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

st.title('Georgia Covid Analysis')
st.write("This app is for exploring Georgia's Covid data")

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
choose_worktype = st.sidebar.selectbox("Go to",['Key metrics','Interactive','Play'])
st.sidebar.header("About")
st.sidebar.info("This app is maintained by Matthew Bailey")

if st.checkbox("Show Data"):
    st.dataframe(covid_data)
    st.write("Dataset contains %s columns and %s rows" % (len(covid_data.columns),len(covid_data)))



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

if(choose_worktype == 'Key metrics'):
    pos_inc_fig = go.Figure()
    pos_inc_fig.update_layout(covid_template)
    pos_inc_fig.update_layout(
        #template=covid_template,
        title="Daily increase of positive cases",
        xaxis_title='Date',
        yaxis_title='Positive Increase',
        legend_title="Legend",
        xaxis=slider_template
        )
    pos_inc_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positiveIncrease'],name='positiveIncrease',text=covid_data['positiveIncrease'],textposition='inside',))
    
    moving_avg_7 = covid_data['positiveIncrease'].rolling(7).mean()
    pos_inc_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

    pos_inc_fig.update_yaxes(automargin=True)
    
    st.plotly_chart(pos_inc_fig, use_container_width=False)


    #TODO Selectbox Positive Cumulative
    if(st.checkbox("Total Positive")):
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
        pos_cumu_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positive'],name='positive',text=covid_data['positive'],textposition='inside',))
    
        moving_avg_7 = covid_data['positive'].rolling(7).mean()
        pos_cumu_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

        pos_cumu_fig.update_yaxes(automargin=True)
    
        st.plotly_chart(pos_cumu_fig, use_container_width=False)

    #TODO Death Increase
    dth_inc_fig = go.Figure()
    dth_inc_fig.update_layout(covid_template)
    dth_inc_fig.update_layout(
        #template=covid_template,
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
    #TODO Selectbox Death Cumulative
    if(st.checkbox("Death Cumulative")):
        dth_cumu_fig = go.Figure()
        dth_cumu_fig.update_layout(covid_template)
        dth_cumu_fig.update_layout(
            #template=covid_template,
            title="Total Deaths",
            xaxis_title='Date',
            yaxis_title='Deaths Cumulative',
            legend_title="Legend",
            xaxis=slider_template
            )
        dth_cumu_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['death'],name='death',text=covid_data['death'],textposition='inside',))
    
        moving_avg_7 = covid_data['death'].rolling(7).mean()
        dth_cumu_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

        dth_cumu_fig.update_yaxes(automargin=True)
    
        st.plotly_chart(dth_cumu_fig, use_container_width=False)

    #TODO Hospitalized Increase
    hosp_inc_fig = go.Figure()
    hosp_inc_fig.update_layout(covid_template)
    hosp_inc_fig.update_layout(
        #template=covid_template,
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

    #TODO Hospitalized Currently
    hosp_cur_fig = go.Figure()
    hosp_cur_fig.update_layout(covid_template)
    hosp_cur_fig.update_layout(
        #template=covid_template,
        title="Currently Hospitalized",
        xaxis_title='Date',
        yaxis_title='Hospitalized',
        legend_title="Legend",
        xaxis=slider_template
        )
    hosp_cur_fig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['hospitalizedCurrently'],name='Death Increase',text=covid_data['hospitalizedCurrently'],textposition='inside',))
    
    moving_avg_7 = covid_data['hospitalizedCurrently'].rolling(7).mean()
    hosp_cur_fig.add_trace(go.Scatter(x=covid_data['date'],y=moving_avg_7, name="7-Day average"))

    hosp_cur_fig.update_yaxes(automargin=True)
    
    st.plotly_chart(hosp_cur_fig, use_container_width=False)

    #TODO Selectbox Hospitalized Cumulative 
    if(st.checkbox("Hospitalized Cumulative")):
        hosp_cumu_fig = go.Figure()
        hosp_cumu_fig.update_layout(covid_template)
        hosp_cumu_fig.update_layout(
            #template=covid_template,
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
        











if(choose_worktype == 'Play'):
    choose_x = st.sidebar.selectbox("Choose the x-data to plot",list(covid_data.columns))
    choose_y= st.sidebar.selectbox("Choose the y-data to plot",list(covid_data.columns))#['New_Deaths','New_Hospitalized',])

    #st.subheader('Georgia Covid data from March 3rd to Present')
    #st.write(covid_data)

    st.header('Data Experimentation')

    #fig = px.bar(covid_data, x=choose_x,y=choose_y,text=choose_y,)

    #st.plotly_chart(fig, use_container_width=True)
    #lineFigure = st.checkbox("Line Figure")
    if st.checkbox("Line Figure"):
        lineFig = px.line(covid_data, x=choose_x, y=choose_y, height=450,width=600)
        lineFig.update_layout(font=dict(size=15))
        st.plotly_chart(lineFig, use_container_width=True)
    moving_avg_7 = covid_data[choose_y].rolling(7).mean()
    if st.checkbox("Scatter Figure"):
        scatterFig = go.Figure()
        scatterFig.add_trace(go.Scatter(x=covid_data[choose_x],y=covid_data[choose_y], name=choose_y ,mode="lines+markers+text"))

        scatterFig.update_layout(
        
        title="Scatter plot of %s by %s" % (choose_y,choose_x),
        xaxis_title=choose_x,
        yaxis_title=choose_y,
        legend_title="Legend",
        font=dict(
            #family="Courier New, monospace",
            size=15,
            color="RebeccaPurple"
        ),
        height=500,
        width=900
        )
        scatterFig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    
                    dict(count=7,
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
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
        )

        #scatterFig.update_layout(
        #autosize=False, 
        #height=450,
        #width=600)

        #moving_avg_7 = covid_data[choose_y].rolling(7).mean()
        scatterFig.add_trace(go.Scatter(x=covid_data[choose_x],y=moving_avg_7, name="7-Day moving average"))
        scatterFig.update_yaxes(automargin=True)
        st.plotly_chart(scatterFig, use_container_width=False)
    if st.checkbox("Bar Figure"):
        barFig = go.Figure()
        barFig.add_trace(go.Bar(x=covid_data[choose_x],y=covid_data[choose_y],name=choose_y,text=covid_data[choose_y],textposition='inside',))

        barFig.add_trace(go.Scatter(x=covid_data[choose_x],y=moving_avg_7, name="7-Day moving average"))
        barFig.update_layout(
        title="Bar plot of %s by %s" % (choose_y,choose_x),
        xaxis_title=choose_x,
        yaxis_title=choose_y,
        legend_title="Legend",
        font=dict(
            #family="Courier New, monospace",
            size=15,
            color="RebeccaPurple"
        ),
        height=700,
        width=1000,
        xaxis=slider_template
        )
        barFig.update_yaxes(automargin=True)
        st.plotly_chart(barFig, use_container_width=False)

    if st.checkbox("Subplots"):

        subFig = make_subplots(rows=1,cols=2)
        #moving_avg_7_ = covid_data[choose_y].rolling(7).mean()
        #subFig.add_trace(go.Scatter(x=covid_data['positive'],y=moving_avg_7_, name="7-Day moving average"))
        

        subFig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positive'],name='Positive cases',text=covid_data['positive'],textposition='inside',),row=1, col=1)

        subFig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positiveIncrease'],name='Positive increase',text=covid_data['positiveIncrease'],textposition='inside',),row=1, col=2)

        subFig.update_layout(
        title="Bar plot of %s by %s" % (choose_y,choose_x),
        xaxis_title=choose_x,
        yaxis_title=choose_y,
        legend_title="Legend",
        font=dict(
            #family="Courier New, monospace",
            size=15,
            color="RebeccaPurple"
        ),
        height=700,
        width=1000,
        )
        subFig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    
                    dict(count=7,
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
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
        )
        subFig.update_yaxes(automargin=True)

        st.plotly_chart(subFig, use_container_width=False)





    #scatterFig.add_trace(go.Scatter(x=covid_data['date'],y=covid_data['positive'], mode="lines+markers"))

    #st.plotly_chart(lineFig, use_container_width=True)
    #st.plotly_chart(scatterFig, use_container_width=True)
    #st.plotly_chart(barFig, use_container_width=True)

