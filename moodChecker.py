import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline


# Read the CSV file and select the param columns
df_raw = pd.read_csv("data/data_moods.csv").dropna(axis=1, how='all')
df = df_raw.dropna()
col_features = df.columns[6:-3]
X = MinMaxScaler().fit_transform(df[col_features])
X2 = np.array(df[col_features])
Y = df['mood']
# Encode the categories
encoder = LabelEncoder()
encoder.fit(Y)
encoded_y = encoder.transform(Y)
# Convert to  dummy (Not necessary in my case)
dummy_y = np_utils.to_categorical(encoded_y)
X_train, X_test, Y_train, Y_test = train_test_split(
    X, encoded_y, test_size=0.2, random_state=15)
target = pd.DataFrame({'mood': df['mood'].tolist(
), 'encode': encoded_y}).drop_duplicates().sort_values(['encode'], ascending=True)


def predict_mood(songs, sp):
    # Join the model and the scaler in a Pipeline
    pip = Pipeline([('minmaxscaler', MinMaxScaler()), ('keras', KerasClassifier(build_fn=base_model, epochs=300,
                                                                                batch_size=64, verbose=0))])
    # Fit the Pipeline
    pip.fit(X2, encoded_y)
    # Obtain the features of the song
    res = {}
    song_ids = []
    for idx, item in enumerate(songs):
        song_ids.append(item['id'])
    meta = sp.tracks(song_ids)
    tracks = sp.audio_features(song_ids)
    for idx, item in enumerate(meta['tracks']):
        # print(item)
        # print(tracks[idx])
        preds = get_songs_features(item,tracks[idx])
        track= []
        track.extend((list(preds.values()), list(preds.keys())))
        metadata = tuple(track)
        preds_features = np.array(metadata[0][7:-2]).reshape(-1, 1).T
        # Predict the features of the song
        results = pip.predict(preds_features)
        preds['mood'] = np.array(
            target['mood'][target['encode'] == int(results)])[0]
        # print("{0} by {1} is a {2} song".format(preds['name'],preds['artist'],preds['mood']))
        res[idx] = (preds)
    return res


def base_model():
    # Create the model
    model = Sequential()
    # Add 1 layer with 8 nodes,input of 4 dim with relu function
    model.add(Dense(8, input_dim=10, activation='relu'))
    # Add 1 layer with output 3 and softmax function
    model.add(Dense(4, activation='softmax'))
    # Compile the model using sigmoid loss function and adam optim
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    return model

def get_songs_features(meta, features):
    # meta
    metadata = {}
    metadata['name'] = meta['name']
    metadata['album'] = meta['album']['name']
    metadata['artist'] = meta['album']['artists'][0]['name']
    metadata['ids'] = meta['id']
    metadata['cover'] = meta['album']['images'][0]['url']
    metadata['release_date'] = meta['album']['release_date']
    metadata['popularity'] = meta['popularity']
    metadata['length'] = meta['duration_ms']
    # features
    metadata['danceability'] = features['danceability']
    metadata['acousticness'] = features['acousticness']
    metadata['energy'] = features['energy']
    metadata['instrumentalness'] = features['instrumentalness']
    metadata['liveness'] = features['liveness']
    metadata['valence'] = features['valence']
    metadata['loudness'] = features['loudness']
    metadata['speechiness'] = features['speechiness']
    metadata['tempo'] = features['tempo']
    metadata['key'] = features['key']
    metadata['time_signature'] = features['time_signature']
    return metadata


def getMood(tracks_data):
    songs_of_mood = []
    percentage = {'Sad': 0, 'Calm': 0, 'Energetic': 0, 'Happy': 0}
    for item in tracks_data:
        if tracks_data[item]['mood'] == 'Sad':
            percentage['Sad'] += 1
        elif tracks_data[item]['mood'] == 'Calm':
            percentage['Calm'] += 1
        elif tracks_data[item]['mood'] == 'Energetic':
            percentage['Energetic'] += 1
        elif tracks_data[item]['mood'] == 'Happy':
            percentage['Happy'] += 1
    most_mood = max(percentage, key=percentage.get)
    total = percentage[most_mood]/30 * 100
    for item in tracks_data:
        if tracks_data[item]['mood'] == most_mood:
            songs_of_mood.append(tracks_data[item])
    return {'songs_of_mood': songs_of_mood, 'total': total, 'mood': most_mood}
