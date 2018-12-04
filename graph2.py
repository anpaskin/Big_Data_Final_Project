import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

plotly.tools.set_credentials_file(username='kaylascharfstein', api_key='QosEetZ0Dao7OFMLXzl6')

def create_graph(feature, label, file):
    df = pd.read_csv(file)
    data = []
    for i in range(0,len(pd.unique(df[label]))):
        trace = {
            "type": 'violin',
            "x": df[label][df[label] == pd.unique(df[label])[i]],
            "y": df[feature][df[label] == pd.unique(df[label])[i]],
            "name": pd.unique(df[label])[i],
            "box": {
                "visible": True
            },
            "meanline": {
                "visible": True
            }
        }
        data.append(trace)

    fig = {
        "data": data,
        "layout": {
            "title": "",
            "yaxis": {
                "zeroline": False,
            }
        }
    }

    py.iplot(fig, validate = False, filename = feature + "_" + label)

create_graph("Energy", "Quartile", "Data2.csv")
create_graph("Energy", "Half", "Data3.csv")
create_graph("Energy", "Track Number", "Data.csv")
create_graph("Popularity", "Quartile", "Data2.csv")
create_graph("Popularity", "Half", "Data3.csv")
create_graph("Popularity", "Track Number", "Data.csv")
create_graph("Sentiment", "Quartile", "Data2.csv")
create_graph("Sentiment", "Half", "Data3.csv")
create_graph("Sentiment", "Track Number", "Data.csv")
