import routes
import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, jsonify,render_template
# from flask import current_app as app


def get_token():
    token_info = session.get(routes.TOKEN_INFO, None)
    if not token_info:
        raise ' exception'
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='6ecede3c0a5b42218103b5df40c15ee1',
        client_secret='b3d80df19e7945378d20484cb7c36f9f',
        redirect_uri=url_for('authorize', _external=True),
        scope='user-top-read'
    )
