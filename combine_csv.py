import csv

song_list = []
with open("New.csv", "r") as f:
    song_reader = csv.reader(f)
    for song in song_reader:
        if song not in song_list:
            song_list.append(song)

with open("Test6.csv", "r") as f:
    song_reader = csv.reader(f)
    for song in song_reader:
        if song not in song_list:
            song_list.append(song)

with open("New.csv", "w") as f:
    song_writer = csv.writer(f)
    for song in song_list:
        song_writer.writerow(song)
