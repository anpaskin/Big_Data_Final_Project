import pandas as pd

# read in data frame of songs to be one hot encoded
song_df = pd.read_csv("New.csv")

# get rid of duplicates
song_df = song_df.drop_duplicates()

# get a list of artists
artists = song_df['Artists']
artist_set = []
for artist in artists:
    temp = artist.split(",")
    for t in temp:
        if t != "" and t not in artist_set:
            artist_set.append(t)

# new data frame with one hot encoded artists
new_df = pd.DataFrame(columns = artist_set)

# one hot encode artists
for artist in artists:
    temp = artist.split(",")
    one_hot = [0 for _ in range(len(artist_set))]
    for t in [x for x in temp if x != ""]:
        # insert 1 at artist index if artist is on current song
        one_hot[artist_set.index(t)] = 1
    new_df = new_df.append(dict(zip(artist_set, one_hot)), ignore_index=True)

# drop unimportant features
song_df = song_df.drop(columns=['Artists', 'Key', 'Mode', 'Time Signature'])

encoded_df = pd.concat([song_df, new_df], axis=1)

# one hot encode albums
album_encoded = pd.get_dummies(encoded_df['Album Name'])

# drop unimportant features
encoded_df = encoded_df.drop(columns=['Album Name', 'Track Name'])

# one hot encoded dataframe
encoded_df = pd.concat([encoded_df, album_encoded], axis=1)

# create csv
encoded_df.to_csv("Data.csv")
