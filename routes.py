import spotipy
from flask import Flask, request, url_for, session, redirect, jsonify,render_template
from flask import current_app as app
# import moodChecker
# import spotifyOAuth

@app.route('/')
def index():
    # try:
    #     token_info = spotifyOAuth.get_token()
    # except:
    #     print('user not logged in')
    #     return redirect('/login')
    return render_template('index.html')