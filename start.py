from tokenize import Single
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv


def append_genre_dataframe(audio_features_df):
    genres = ["ceilidh", "irish neo-traditional", "irish dance", "irish banjo",
              "irish accordion", "irish fiddle ", "irish flute"]

    for genre in genres:
        neo_trad_results = spotify.search(q='genre:"' + genre + '"', limit=50)
        # Parse artist name and track URI from API response.
        # Only retaining the first artist from for each track (some tracks may have multiple artists attached)
        tracks = [dict(uri=x['uri'], artist=x['artists'][0]['name'])
                  for x in neo_trad_results['tracks']['items']]
        # Retrieve audio_features data for each track and persist artist name in dictionary
        track_audio_features = [dict(spotify.audio_features(track['uri'])[
                                     0], **{'artist': track['artist']}) for track in tracks]
        # Remove tracks which are not instrumental and append genre to dictionary
        track_audio_features = [dict(track, **{'genre': genre})
                                for track in track_audio_features if track['speechiness'] < 0.33]
        # Convert dictionary to dataframe and append to audio_features_df
        tmp_df = pd.DataFrame(track_audio_features)
        audio_features_df = audio_features_df.append(tmp_df)

    return audio_features_df


def append_ceili_band_dataframe(audio_features_df):
    # Albums from the following All-Ireland winning Céilí bands:
    # 'Tulla Céilí Band, 'Kilfenora Céilí Band', 'Bridge Céilí Band', 'Blackwater Céilí Band', Shandrum Céilí Band, Dartry Céilí Band
    ceili_band_albums = [{'artist': 'Tulla Céilí Band', 'album_id': 'spotify:album:6oACn8LTzDhv8O4XxXynXK', 'album_name': 'A Celebration of 50 Years'}, {'artist': 'Kilfenora Céilí Band', 'album_id': 'spotify:album:7bZ3TaA6Uwb8kseVZkleBR', 'album_name': 'Century'}, {'artist': 'Bridge Céilí Band', 'album_id': 'spotify:album:5NoFcJyqYsRRHavObhglG5', 'album_name': 'Irish Ceili'}, {
        'artist': 'Blackwater Céilí Band', 'album_id': 'spotify:album:7l2nYSlqFPtMpDRFznwly6', 'album_name': 'Music In The Valley'}, {'artist': 'The Shandrum Céilí Band', 'album_id': 'spotify:album:2mMz3aUmTWlU56GHzrnv9n', 'album_name': 'The Dawn'}, {'artist': 'Dartry Ceili Band', 'album_id': 'spotify:album:4pUVU9j3H2DDF7wp8Y8Z6b', 'album_name': 'The Killavil Post'}]
    # artists = [ spotify.album(album)['artists'][0]['name'] for album in ceili_band_albums ]
    grouped_album_tracks = [dict(spotify.album_tracks(
        album['album_id']), **{'artist': album['artist']}) for album in ceili_band_albums]
    track_audio_features = [dict(spotify.audio_features(single_track['uri'])[
                                 0], **{'artist': album_tracks['artist']}) for album_tracks in grouped_album_tracks for single_track in album_tracks['items']]

    track_audio_features = [dict(track, **{'genre': 'All Ireland Céilí Bands'})
                            for track in track_audio_features if track['speechiness'] < 0.33]
    tmp_df = pd.DataFrame(track_audio_features)
    audio_features_df = audio_features_df.append(tmp_df)

    return audio_features_df


if __name__ == "__main__":
    # Load 'SPOTIPY_CLIENT_ID' and 'SPOTIPY_CLIENT_SECRET' from .env
    load_dotenv()
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials())

    audio_features_df = pd.DataFrame()
    audio_features_df = append_genre_dataframe(audio_features_df)
    audio_features_df = append_ceili_band_dataframe(audio_features_df)
    audio_features_df.to_csv('audio_features.csv')


# Additional Insights?
# - Most represented artists in modern spotify?
# - How many unique key signatures among all tracks? How are they distributed?
# - Discrepancies between Spotify tempo and real tempo
# Include more classic recordings?
# 'Michael Coleman' - 'Ceoltóir Mórthionchair Na hAoise (1891-1945)' - https://open.spotify.com/album/38Idpa2H1iuo1Yp3ojHtXK?si=FBf89tscTYObSk7an0NjFg
# 'Willie Clancy - 'The Gold Ring' - https://open.spotify.com/album/0O7PGfK03BeWdIz37Y694X?si=WlW71Y_hTC6W4km2-Ob17w
# 'Seamus Ennis' - 'The Wandering Minstrel' - https://open.spotify.com/album/59uIc2pxNlQeGYgs9sZ66v?si=Lep1rrGyQ_SJmNoPyRDrLg
