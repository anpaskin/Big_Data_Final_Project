import pandas as pd

data = pd.read_csv("Data.csv")

new_col = []

for total_track, track_number in zip(data["Total Tracks on Album"], data["Track Number"]):
    f = float(track_number)/float(total_track)
    # if f >= 0 and f < .25:
    #     new_col.append(1)
    # elif f >= .25 and f < .5:
    #     new_col.append(2)
    # elif f >= .5 and f < .75:
    #     new_col.append(3)
    # else:
    #     new_col.append(4)
    if f >= 0 and f < .5:
        new_col.append(0)
    else:
        new_col.append(1)

data = pd.concat([data, pd.DataFrame({"Half" : new_col})], axis = 1)
data = data.drop(columns = ["Track Number", "Total Tracks on Album"])
data.to_csv("Data3.csv")
