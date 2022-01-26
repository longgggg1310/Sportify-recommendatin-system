from flask import Flask, json, render_template, request,jsonify
import pandas as pd
import random
import numpy as np
from numpy.linalg import norm
import tekore as tk

def authorize():
     CLIENT_ID = "0129ed4fb2f84f728d52c304561fce9d"
     CLIENT_SECRET = "e0268e4cb35445aca8bdb6aacd0b8aad"
     app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
     return tk.Spotify(app_token)

def recommend(track_id):
    global result
    ref_df =df
    # Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    print(f"mood_vec for {track_id}: {track_moodvec}")

    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    # If the input track is in the reference set, it will have a distance of 0, but should not be recommendet
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    result =ref_df_sorted.iloc[:10]

    # Return n recommendations
    return result

app = Flask(__name__)
df = pd.read_csv("valence_arousal_dataset1.csv")
df["mood_vec"] = df[["valence", "energy"]].values.tolist()
sp = authorize()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/about',methods=['POST'])
def getvalue():
    track_id = request.form['moviename']
    recommend(track_id)
    df=result
    return render_template('result.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=False)
