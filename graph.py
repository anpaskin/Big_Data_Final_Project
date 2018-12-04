import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

# create bar plot in plotly showing accuracy across different classifiers and labeling mechanisms

plotly.tools.set_credentials_file(username='kaylascharfstein', api_key='QosEetZ0Dao7OFMLXzl6')

trace1 = go.Bar(
    x=['Track Number', 'Quartile', 'Half'],
    y=[0.081465425, 0.253018069, 0.507755128],
    name='K Nearest Neighbors'
)
trace2 = go.Bar(
    x=['Track Number', 'Quartile', 'Half'],
    y=[0.059036924,	0.255705577, 0.48533729],
    name='Neural Network'
)

trace3 = go.Bar(
    x=['Track Number', 'Quartile', 'Half'],
    y=[0.02, 0.25, 0.5],
    name='Random'
)

data = [trace1, trace2, trace3]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='grouped-bar')
