import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo

# Load CSV file from Datasets folder

df = pd.read_csv('../Datasets/Olympic2016Rio.csv')

# Removing empty spaces from NOC column to avoid errors
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Creating sum of number of Medals group by NOC Column
new_df = df.groupby(['NOC']).agg({'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum', 'Total': 'sum'}).reset_index()

# Sorting values and select 20 first value
new_df = new_df.sort_values(by=['Total'],
                            ascending=[False]).head(20).reset_index()

# Preparing data
trace1 = go.Bar(x=new_df['NOC'], y=new_df['Gold'], name='Gold',
                marker={'color': '#ffff00'})
trace2 = go.Bar(x=new_df['NOC'], y=new_df['Silver'], name='Silver',
                marker={'color': '#cccccc'})
trace3 = go.Bar(x=new_df['NOC'], y=new_df['Bronze'], name='Bronze',
                marker={'color': '#cc9900'})
data = [trace1, trace2, trace3]

# Preparing layout
layout = go.Layout(title='Gold, Silver, and Bronze Medals by Country', xaxis_title="NOC",
                   yaxis_title="Medals", barmode='stack')

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='stackbarchart.html')
