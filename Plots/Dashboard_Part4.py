import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
from dash.exceptions import PreventUpdate

df1 = pd.read_csv('../Datasets/Weather2014-15.csv')
df2 = pd.read_csv('../Datasets/Olympic2016Rio.csv')

app = dash.Dash()

# Bar chart data
#Pulls the country names from the file, then iterates through the result and puts it in an array. This array is then
#used to create the options dropdown in the interactive bar chart

options_df = pd.read_csv('../Datasets/Olympic2016Rio.csv', usecols=['NOC'])
barchart_options = []
for x in range(0,options_df.size):
    barchart_options.append({'label': options_df.iloc[x]['NOC'], 'value': options_df.iloc[x]['NOC']})

print(barchart_options)

barchart_df = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['NOC'])['Total'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Total'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Total'])]

# Stack bar chart data
stackbarchart_df = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df = stackbarchart_df.groupby(['NOC']).agg(
    {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum', 'Total': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'],
                            ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold',
                marker={'color': '#ffff00'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver',
                marker={'color': '#cccccc'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze',
                marker={'color': '#cc9900'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df1
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['date'], y=line_df['actual_max_temp'], mode='lines', name='Max Temp')]

# Multi Line Chart
multiline_df = df1
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_max_temp'], mode='lines', name='Max')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_min_temp'], mode='lines', name='Min')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines', name='Mean')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df1
#This throws an error???
#bubble_df = df1.apply(lambda y: y.str.strip() if y.dtype == "object" else y)
bubble_df = bubble_df.groupby(['month']).agg(
    {'actual_max_temp': 'mean', 'actual_min_temp': 'mean', 'actual_mean_temp': 'mean'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['actual_max_temp'],
               y=bubble_df['actual_min_temp'],
               text=bubble_df['month'], mode='markers',
           marker=dict(size=bubble_df['actual_mean_temp'],
                       color=bubble_df['actual_mean_temp'],
                       showscale=True))]


# Heatmap
heatmap_df = df1
heatmap_df['date'] = pd.to_datetime(heatmap_df['date'])
data_heatmap = [go.Heatmap(x=heatmap_df['day'],
                   y=heatmap_df['month'],
                   z=heatmap_df['record_max_temp'].values.tolist(),
                   colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Lab Part 4: Olympic Bar Charts and Weather Other Charts', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the Total Olympic Medals by Country'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a Country', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-country',
        options=barchart_options,
        value='United States(USA)',
        placeholder="Select a Country"
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the Total Olympic Medals by Country, limited by the top 20 countries.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Total Olympic Medals by Country',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Total Medals'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents the Gold, Silver, and Bronze Medals by Country, limited to the top 20 countries.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Gold, Silver, and Bronze Medals by Country',
                                      xaxis={'title': 'NOC'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represents the Max Temperatures for Each Month From 2014-07 to 2015-06.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Max Temperatures for Each Month From 2014-07 to 2015-06',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Max Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This multi-line chart represents the Min, Max, and Mean Temps by Month From 2014-07 to 2015-06.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Min, Max, and Mean Temps by Month From 2014-07 to 2015-06',
                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represents the range of maximum and minimum temps per month, across one year.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Max and Min Temps by Month',
                                      xaxis={'title': 'Maximum'}, yaxis={'title': 'Minimum'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represents the Max Temperatures by Month and Day of Week.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Max Temperatures by Month and Day of Week',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month'})
              }
              )
])



@app.callback(Output('graph1', 'figure'),
              [Input('select-country', 'value')])
def update_figure(selected_country):
    filtered_df = df2[df2['NOC'] == selected_country]

    new_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data_interactive_barchart = [go.Bar(x=new_df['NOC'], y=new_df['Total'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Gold Medals won by '+selected_country,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of Gold Medals'})}


if __name__ == '__main__':
    app.run_server()
