import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')
df['date'] = pd.to_datetime(df['date'])

# Preparing data
data = [go.Scatter(x=df['date'], y=df['actual_max_temp'], mode='lines', name='Max Temp')]

# Preparing layout
layout = go.Layout(title='Max Temperatures for Each Month From 2014-07 to 2015-06', xaxis_title="Month",
                   yaxis_title="Max Temperature")

#Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='linechart.html')