#!/usr/bin/env python
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np


#Loading data
df = pd.read_csv('nama_10_gdp_1_Data.csv')

#Cleaning data
eu_data = [
    "European Union (current composition)",
    "European Union (without United Kingdom)",
    "European Union (15 countries)",
    "Euro area (EA11-2000, EA12-2006, EA13-2007, EA15-2008, EA16-2010, EA17-2013, EA18-2014, EA19)",
    "Euro area (19 countries)",
    "Euro area (12 countries)"]

df_clean = df[df['Value'] != ":"] #Filtering out not existing values

df_clean = df_clean[~df_clean['GEO'].isin(eu_data)] #Filtering out aggregated EU values

#Creating options for dropdowns
available_indicators = df_clean['NA_ITEM'].unique()
available_units = df_clean['UNIT'].unique()
available_countries = df_clean['GEO'].unique()

#Starting the app
app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#Creating app layout
app.layout = html.Div([
    html.Div([
        #Layout for Task 1
        html.H1( 
            children = "Graph #1",
            style = {'text-align': 'center'}
        ),       
        html.Div([ #First dropdown / radioitem element
            html.H1(
                children = "Select Indicator 1",
                style = {'font-size': '12px', 'text-align': 'center'}
            ),     
            dcc.Dropdown( 
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of services'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '33.33%', 'display': 'inline-block'}),

        html.Div([ #Second dropdown / radioitem element
            html.H1(
                children = "Select Indicator 2",
                style = {'font-size': '12px', 'text-align': 'center'}
            ),  
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '33.33%', 'margin-left': 'auto', 'margin-right': 'auto','display': 'inline-block'}),
        
        html.Div([ #First dropdown element
            html.H1(
                children = "Select Unit",
                style = {'font-size': '12px', 'text-align': 'center'}
            ),  
            dcc.Dropdown(
                id='select-unit',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )
        ],style={'width': '33.33%', 'float': 'right', 'display': 'inline-block'})
        
    ]), 
    
    dcc.Graph(id='indicator-graphic'), #Creating graph

    html.Div([
        html.H1(
            children = "Select Year",
            style = {'font-size': '12px', 'text-align': 'center'}
            ), 
    
        dcc.Slider( #Creating slider
            id='year--slider',
            min=df_clean['TIME'].min(),
            max=df_clean['TIME'].max(),
            value=df_clean['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df_clean['TIME'].unique()}
        ),
    ],
        style={'width': '90%', 'margin':'auto'}),

    #Layout for Task 2
    html.Div([
        html.H1(
            children = "__________________________________________________",
            style = {'text-align': 'center'}
        ),  
        html.H1(
            children = "Graph #2",
            style = {'text-align': 'center'}
        ),  
        
        html.Div([ #First dropdown element
            html.H1(
                children = "Select Country",
                style = {'font-size': '12px', 'text-align': 'center'}
            ),     
            dcc.Dropdown(
                id='2-select-country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='Spain'
            ),
            html.H1( #For layout alignment of dropdown boxes
                children = "x",
                style = {'font-size': '9px', 'text-align': 'center', 'color': 'white'}
            )
        ],
        style={'width': '33.33%', 'margin-left': 'auto', 'margin-right': 'auto','display': 'inline-block'}),

        html.Div([ #Second dropdown / radioitem element
            html.H1(
                children = "Select Indicator",
                style = {'font-size': '12px', 'text-align': 'center'}
            ),  
            dcc.Dropdown(
                id='2-select-indicator',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods'
            ),
            dcc.RadioItems(
                id='2-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '33.33%', 'margin-left': 'auto', 'margin-right': 'auto','display': 'inline-block'}),
        
        html.Div([ #Third dropdown element
            html.H1(
                children = "Select Unit",
                style = {'font-size': '12px', 'text-align': 'center'}
            ),  
            dcc.Dropdown(
                id='2-select-unit',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )
        ],style={'width': '33.33%', 'float': 'right', 'display': 'inline-block'})
    ]), 

    dcc.Graph(id='2-indicator-graphic'), #Creating graph

])
   

#Interactivity for Task 1
@app.callback( #Linking dropdown selections (ids from above) as inputs for graph
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('select-unit', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, unit_type, 
                 xaxis_type, yaxis_type,
                 year_value):
   
    dff = df_clean[(df_clean['TIME'] == year_value) & (df_clean['UNIT'] == unit_type)] #Filtering for time and unit
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'], #Getting value for selected x indicator
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'], #Getting value for selected y indicator
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'], 
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout( #Adding column names and linear / log layouts
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 90, 'b': 60, 't': 40, 'r': 90},
            hovermode='closest'
        )
    }

#Interactivity for Task 2
@app.callback( #Linking dropdown selections (ids from above) as inputs for graph
    dash.dependencies.Output('2-indicator-graphic', 'figure'),
    [dash.dependencies.Input('2-select-indicator', 'value'),
     dash.dependencies.Input('2-select-country', 'value'),
     dash.dependencies.Input('2-select-unit', 'value'),
     dash.dependencies.Input('2-yaxis-type', 'value'),])
def update_graph(indicator, country, unit_type2,
                 yaxis_type2):

    dff = df_clean[(df_clean['GEO'] == country) #Filtering for country, indicator and selected unit
                   & (df_clean['NA_ITEM'] == indicator) 
                   & (df_clean['UNIT'] == unit_type2)]
    
    return {
        'data': [go.Scatter(
            x=dff['TIME'], #Getting respective year as x value
            y=dff['Value'], #Getting respective value as y value
            text=dff['Value'],
            mode='lines',
        )],
        'layout': go.Layout(
            xaxis={
                'title': 'Years',
            },
            yaxis={
                'title': indicator,
                'type': 'linear' if yaxis_type2 == 'Linear' else 'log'
            },
            margin={'l': 90, 'b': 40, 't': 40, 'r': 90},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()

