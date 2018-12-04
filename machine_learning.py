import pandas as pd

song_df = pd.read_csv("New.csv")
song_df = song_df.drop_duplicates()
artists = song_df['Artists']
artist_set = []
for artist in artists:
    temp = artist.split(",")
    for t in temp:
        if t != "" and t not in artist_set:
            artist_set.append(t)

new_df = pd.DataFrame(columns = artist_set)

for artist in artists:
    temp = artist.split(",")
    one_hot = [0 for _ in range(len(artist_set))]
    for t in [x for x in temp if x != ""]:
        one_hot[artist_set.index(t)] = 1
    new_df = new_df.append(dict(zip(artist_set, one_hot)), ignore_index=True)

song_df = song_df.drop(columns=['Artists', 'Key', 'Mode', 'Time Signature'])
encoded_df = pd.concat([song_df, new_df], axis=1)

album_encoded = pd.get_dummies(encoded_df['Album Name'])
encoded_df = encoded_df.drop(columns=['Album Name', 'Track Name'])
encoded_df = pd.concat([encoded_df, album_encoded], axis=1)

encoded_df.to_csv("Data.csv")
