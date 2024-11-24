import requests
import json

BASE_URL = 'http://localhost:5000'

def print_response(response):
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

# 1. Create Songs
songs = [
    {
        "name": "Bohemian Rhapsody",
        "artist": "Queen",
        "genre": "Rock"
    },
    {
        "name": "Stairway to Heaven",
        "artist": "Led Zeppelin",
        "genre": "Rock"
    },
    {
        "name": "Yesterday",
        "artist": "The Beatles",
        "genre": "Rock"
    }
]

created_songs = []
print("Creating songs...")
for song in songs:
    response = requests.post(f"{BASE_URL}/songs", json=song)
    print_response(response)
    created_songs.append(response.json())

# 2. Create a Playlist
print("\nCreating playlist...")
playlist_data = {
    "name": "Classic Rock Hits"
}
response = requests.post(f"{BASE_URL}/playlists", json=playlist_data)
print_response(response)
playlist = response.json()

# 3. Add Songs to Playlist
print("\nAdding songs to playlist...")
for song in created_songs:
    response = requests.post(
        f"{BASE_URL}/playlists/{playlist['id']}/songs/{song['id']}"
    )
    print_response(response)

# 4. Get Playlist
print("\nGetting playlist...")
response = requests.get(f"{BASE_URL}/playlists/{playlist['id']}")
print_response(response)

# 5. Sort Playlist by different criteria
for sort_key in ['name', 'artist', 'genre']:
    print(f"\nSorting playlist by {sort_key}...")
    response = requests.post(
        f"{BASE_URL}/playlists/{playlist['id']}/sort",
        json={"sort_key": sort_key}
    )
    print_response(response)

# 6. Remove a Song from Playlist
print("\nRemoving first song from playlist...")
response = requests.delete(
    f"{BASE_URL}/playlists/{playlist['id']}/songs/{created_songs[0]['id']}"
)
print_response(response)

# 7. Get Final Playlist State
print("\nFinal playlist state:")
response = requests.get(f"{BASE_URL}/playlists/{playlist['id']}")
print_response(response)