import CovidAPI as ca
import json
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title('Covid Data Analysis')
st.write("This app is for exploring Georgia's Covid data")

def data_retrieval():
    newRun = ca.CovidAPI()
    newRun.setDataPath("data/Georgia_Covid.json")
    newRun.updateData("ga")
    
@st.cache(ttl=60*60*24)
def load_data(filepath):
    data_retrieval()
    data = pd.read_json(filepath)
    #data['date'] = data['date'].apply(pd.datetime)
    data['date'] = pd.to_datetime(data['date'], format="%Y%m%d")
    data = data.dropna(axis='columns', how='all')
    data = data.loc[:, (data != 0).any(axis=0)]
    #data.drop(columns=['onVentilatorCumulative','recovered','onVentilatorCurrently','inIcuCurrently'])
    return data

covid_data = load_data("data\Georgia_Covid.json")#load_data("Georgia_Covid.json")
choose_worktype = st.sidebar.selectbox("Select Work Type",['Work','Play'])
if st.checkbox("Show Data"):
    st.write(covid_data)
    st.write("Dataset contains %s columns and %s rows" % (len(covid_data.columns),len(covid_data)))
#fig = px.line(covid_data, x='date',y='positive')
#st.plotly_chart(fig)
if(choose_worktype == 'Work'):
    barFig = go.Figure()
    barFig.add_trace(go.Bar(x=covid_data['date'],y=covid_data['positiveIncrease'],name='positiveIncrease',text=covid_data['positiveIncrease'],textposition='inside',))
    movingAvg_7 = covid_data['positiveIncrease'].rolling(7).mean()
    barFig.add_trace(go.Scatter(x=covid_data['date'],y=movingAvg_7, name="7-Day moving average"))        
    barFig.update_layout(
    title="Daily increase of positive cases",
    xaxis_title='Date',
    yaxis_title='Positive Increase',
    legend_title="Legend",
    font=dict(
        #family="Courier New, monospace",
        size=15,
        color="RebeccaPurple"
    ),
    height=600,
    width=1000,
    )
    barFig.update_layout(
    xaxis=dict(
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
    )
    barFig.update_yaxes(automargin=True)

    st.plotly_chart(barFig, use_container_width=False)
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
    movingAvg_7 = covid_data[choose_y].rolling(7).mean()
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

        #movingAvg_7 = covid_data[choose_y].rolling(7).mean()
        scatterFig.add_trace(go.Scatter(x=covid_data[choose_x],y=movingAvg_7, name="7-Day moving average"))
        scatterFig.update_yaxes(automargin=True)
        st.plotly_chart(scatterFig, use_container_width=False)
    if st.checkbox("Bar Figure"):
        barFig = go.Figure()
        barFig.add_trace(go.Bar(x=covid_data[choose_x],y=covid_data[choose_y],name=choose_y,text=covid_data[choose_y],textposition='inside',))

        barFig.add_trace(go.Scatter(x=covid_data[choose_x],y=movingAvg_7, name="7-Day moving average"))
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
        )
        barFig.update_layout(
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
        barFig.update_yaxes(automargin=True)
        st.plotly_chart(barFig, use_container_width=False)

    #scatterFig.add_trace(go.Scatter(x=covid_data['date'],y=covid_data['positive'], mode="lines+markers"))

    #st.plotly_chart(lineFig, use_container_width=True)
    #st.plotly_chart(scatterFig, use_container_width=True)
    #st.plotly_chart(barFig, use_container_width=True)

