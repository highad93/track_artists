from time import sleep
from get_spotify_creds import get_spotify_creds
import csv
import requests
from tqdm import tqdm


class apiCounter:
    """This class simply counts the number of calls to API to prevent rate limiting """
    def __init__(self, limit: int = 60, timeout: int = 60):
        self.limit = limit
        self.timeout = timeout
        self.count = 0

    def increment(self):
        self.count += 1
        if self.count == self.limit:
            print("\nAPI limit reached. Sleeping...")
            sleep(self.timeout)
            self.count = 0


def main(fname: str = "songs.csv", i:int = 0):
    with open(fname, "w") as f:
        writer = csv.writer(f)
        header = [
            "song_id",
            "track_name",
            "artist_name",
            "album_name",
            "track_popularity",
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "duration",
            "tempo",
            "time_signature",
            "playlist_id",
        ]

        writer.writerow(header)

    apiManager = apiCounter()
    access_token = get_spotify_creds()
    apiManager.increment()

    playlist_ids = []
    with open("../Data/playlist_lst.csv", "r") as f:
        next(f)
        for line in f:
            playlist_ids.append(line)

    playlist_ids = playlist_ids[i:]

    for playlist_id in tqdm(playlist_ids):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id.strip()}/tracks/"
        headers = {"Authorization": "Bearer " + access_token}
        params = {"limit": 50}
        response = requests.get(url, headers=headers, params=params).json()
        apiManager.increment()
        try:
            song_ids = [item["track"]["id"] for item in response["items"]]
        except TypeError: #I guess playlists can be empty.
            continue
        except KeyError:
            print(response)
            quit()
        filtered_song_ids = [id for id in song_ids if id is not None]
        try:
            song_ids_str = ",".join(filtered_song_ids)
        except TypeError:
            print(filtered_song_ids)
            quit()

        song_url = f"https://api.spotify.com/v1/tracks?ids={song_ids_str}"

        response_song = requests.get(song_url, headers=headers).json()

        if "tracks" not in response_song:
            continue #sometimes tracks don't exist I guess.
        response_song = response_song["tracks"]

        apiManager.increment()
        feature_url = f"https://api.spotify.com/v1/audio-features?ids={song_ids_str}"
        response_feature = requests.get(feature_url, headers=headers).json()
        if "audio_features" not in response_feature: #ignore songs without audio features
            if "error" in response_feature:
                print(response_feature)
                quit()
            continue
        response_feature = response_feature["audio_features"]

        apiManager.increment()

        for song_id, song, feature in zip(
            song_ids, response_song, response_feature
        ):
            if song is not None and feature is not None:
                if "name" in song:
                    track_name = song["name"]
                    artist_name = song["artists"][0]["name"]
                    album_name = song["album"]["name"]
                    track_popularity = song["popularity"]
                    danceability = feature["danceability"]
                    energy = feature["energy"]
                    key = feature["key"]
                    loudness = feature["loudness"]
                    mode = feature["mode"]
                    speechiness = feature["speechiness"]
                    acousticness = feature["acousticness"]
                    instrumentalness = feature["instrumentalness"]
                    liveness = feature["liveness"]
                    valence = feature["valence"]
                    tempo = feature["tempo"]
                    duration = feature["duration_ms"]
                    time_signature = feature["time_signature"]

                    with open(fname, "a") as f:
                        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
                        writer.writerow(
                            [
                                song_id,
                                track_name,
                                artist_name,
                                album_name,
                                track_popularity,
                                danceability,
                                energy,
                                key,
                                loudness,
                                mode,
                                speechiness,
                                acousticness,
                                instrumentalness,
                                liveness,
                                valence,
                                duration,
                                tempo,
                                time_signature,
                                playlist_id.strip(),
                            ]
                        )
            else:
                continue


if __name__ == "__main__":
    main("fname.csv")
