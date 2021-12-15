import spotipy
from flask import Flask, request, url_for, session, redirect, jsonify,render_template
from flask import current_app as app
import moodChecker
import spotifyOAuth

SESSION_COOKIE_NAME = 'spotify-api'
TOKEN_INFO = 'token_info'

@app.route('/spotifyLogin')
def spotifyLogin():
    sp_oauth = spotifyOAuth.create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/login')
def login():
    try:
        token_info = spotifyOAuth.get_token()
        return redirect('/')
    except:
        # print('user not logged in')
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 

@app.route('/')
def index():
    try:
        token_info = spotifyOAuth.get_token()
    except:
        # print('user not logged in')
        return redirect('/login')
    return render_template('index.html')
    

@app.route('/authorize')
def authorize():
    sp_oauth = spotifyOAuth.create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('index'))

@app.route('/getTracks',  methods=['POST','GET'])
def getTracks():
    token_info = spotifyOAuth.get_token()
    top_30 = []
    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_30_tracks = sp.current_user_top_tracks(limit=30,offset=0,time_range="medium_term")
    top_30 = moodChecker.predict_mood(top_30_tracks['items'],sp)
    percentage = moodChecker.getMood(top_30)
    result = {'top_10': top_30, 'percentage': percentage['total'], 'mood_songs': percentage['songs_of_mood'], 'user_mood': percentage['mood']}
    print('done')
    return {'status' :200, 'message':'success', 'result':result}
