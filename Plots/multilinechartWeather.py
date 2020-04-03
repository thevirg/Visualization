import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')
df['date'] = pd.to_datetime(df['date'])

# Preparing data
trace1 = go.Scatter(x=df['date'], y=df['actual_max_temp'], mode='lines', name='Max')
trace2 = go.Scatter(x=df['date'], y=df['actual_min_temp'], mode='lines', name='Min')
trace3 = go.Scatter(x=df['date'], y=df['actual_mean_temp'], mode='lines', name='Mean')
data = [trace1,trace2,trace3]

# Preparing layout
layout = go.Layout(title='Min, Max, and Mean Temps by Month From 2014-07 to 2015-06', xaxis_title="Month",
                   yaxis_title="Temperature")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='multilinechart.html')