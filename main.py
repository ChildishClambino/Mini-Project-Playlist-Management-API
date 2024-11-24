from flask import Flask, request, jsonify
from collections import deque
from typing import Dict, List, Optional
import heapq
import time

app = Flask(__name__)

class Song:
    def __init__(self, id: str, name: str, artist: str, genre: str):
        self.id = id
        self.name = name
        self.artist = artist
        self.genre = genre
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'genre': self.genre
        }

class Node:
    def __init__(self, song: Song):
        self.song = song
        self.next = None
        self.prev = None

class PlaylistLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        
    def append(self, song: Song):
        new_node = Node(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        
    def remove(self, song_id: str) -> bool:
        current = self.head
        while current:
            if current.song.id == song_id:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                    
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                    
                self.size -= 1
                return True
            current = current.next
        return False
    
    def to_list(self) -> List[Dict]:
        result = []
        current = self.head
        while current:
            result.append(current.song.to_dict())
            current = current.next
        return result

class Playlist:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.songs = PlaylistLinkedList()
        self.recently_played = deque(maxlen=10)  # Queue for recently played songs
        self.song_index = {}  # Hash table for O(1) song lookup
        
    def add_song(self, song: Song) -> bool:
        if song.id in self.song_index:
            return False
        self.songs.append(song)
        self.song_index[song.id] = song
        return True
        
    def remove_song(self, song_id: str) -> bool:
        if song_id not in self.song_index:
            return False
        self.songs.remove(song_id)
        del self.song_index[song_id]
        return True
    
    def get_song(self, song_id: str) -> Optional[Song]:
        return self.song_index.get(song_id)
    
    def play_song(self, song_id: str):
        if song := self.get_song(song_id):
            self.recently_played.append(song)
    
    def sort_songs(self, key: str = 'name'):
        # Convert linked list to array for sorting
        songs_list = self.songs.to_list()
        
        # QuickSort implementation for sorting songs
        def quicksort(arr: List[Dict], low: int, high: int):
            def partition(low: int, high: int) -> int:
                pivot = arr[high][key]
                i = low - 1
                
                for j in range(low, high):
                    if arr[j][key] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                return i + 1
            
            if low < high:
                pi = partition(low, high)
                quicksort(arr, low, pi - 1)
                quicksort(arr, pi + 1, high)
        
        quicksort(songs_list, 0, len(songs_list) - 1)
        
        # Rebuild linked list with sorted songs
        self.songs = PlaylistLinkedList()
        for song_dict in songs_list:
            song = Song(**song_dict)
            self.songs.append(song)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'songs': self.songs.to_list(),
            'recently_played': [song.to_dict() for song in self.recently_played]
        }

# In-memory storage
songs_db = {}
playlists_db = {}

# API Endpoints
@app.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    song = Song(
        id=str(time.time()),  # Simple ID generation
        name=data['name'],
        artist=data['artist'],
        genre=data['genre']
    )
    songs_db[song.id] = song
    return jsonify(song.to_dict()), 201

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = songs_db.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    return jsonify(song.to_dict())

@app.route('/songs/<song_id>', methods=['PUT'])
def update_song(song_id):
    song = songs_db.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    
    data = request.get_json()
    song.name = data.get('name', song.name)
    song.artist = data.get('artist', song.artist)
    song.genre = data.get('genre', song.genre)
    return jsonify(song.to_dict())

@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    if song_id not in songs_db:
        return jsonify({'error': 'Song not found'}), 404
    del songs_db[song_id]
    return '', 204

@app.route('/playlists', methods=['POST'])
def create_playlist():
    data = request.get_json()
    playlist = Playlist(
        id=str(time.time()),
        name=data['name']
    )
    playlists_db[playlist.id] = playlist
    return jsonify(playlist.to_dict()), 201

@app.route('/playlists/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    playlist = playlists_db.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(playlist.to_dict())

@app.route('/playlists/<playlist_id>/songs/<song_id>', methods=['POST'])
def add_song_to_playlist(playlist_id, song_id):
    playlist = playlists_db.get(playlist_id)
    song = songs_db.get(song_id)
    
    if not playlist or not song:
        return jsonify({'error': 'Playlist or song not found'}), 404
        
    if playlist.add_song(song):
        return jsonify(playlist.to_dict())
    return jsonify({'error': 'Song already in playlist'}), 400

@app.route('/playlists/<playlist_id>/songs/<song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    playlist = playlists_db.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
        
    if playlist.remove_song(song_id):
        return jsonify(playlist.to_dict())
    return jsonify({'error': 'Song not found in playlist'}), 404

@app.route('/playlists/<playlist_id>/sort', methods=['POST'])
def sort_playlist(playlist_id):
    playlist = playlists_db.get(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    
    data = request.get_json()
    sort_key = data.get('sort_key', 'name')
    if sort_key not in ['name', 'artist', 'genre']:
        return jsonify({'error': 'Invalid sort key'}), 400
        
    playlist.sort_songs(sort_key)
    return jsonify(playlist.to_dict())

if __name__ == '__main__':
    app.run(debug=True)