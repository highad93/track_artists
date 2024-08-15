"""
This script gets the spotify access token
"""

from hidden import CLIENT_ID, CLIENT_SECRET
import requests


def get_spotify_creds():
    """
    This function retrieves the API access token using hidden.py. (Individuals use own credentials)
    :return:
        access_token (str) -- API access token
    """
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json()
    access_token = response["access_token"]

    return access_token

if __name__ == "__main__":
    access_token = get_spotify_creds()
    print(access_token)
