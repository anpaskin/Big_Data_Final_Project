import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd

plotly.tools.set_credentials_file(username='eemerson97', api_key='bg9YTyUuhzEdMoVQtWBj')

def create_box_graph(feature, label, file):
    df = pd.read_csv(file)
    data = []
    for i in range(0,len(pd.unique(df[label]))):
        trace = {
            "type": 'box',
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

    
create_box_graph("Duration (ms)", "Quartile", "Data2.csv")
create_graph("Duration (ms)", "Half", "Data3.csv")
create_box_graph("Duration (ms)", "Track Number", "Data.csv")
