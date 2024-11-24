Mini-Project-Playlist-Management-API
This is a comprehensive playlist management system that incorporates several data structures and algorithms

Description
Data Structures Used:

Doubly Linked List (PlaylistLinkedList): For efficient insertion and removal of songs
Hash Table (song_index): For O(1) song lookup within playlists
Queue (deque): For tracking recently played songs with a fixed size
Custom Node class: For implementing the linked list structure


Algorithms Implemented:

QuickSort: For efficient sorting of songs (O(n log n) average case)
Binary Search could be added for searching through sorted playlists
Hash-based searching: O(1) lookup for songs using the song_index


Key Features:

CRUD operations for both songs and playlists
Efficient song addition and removal from playlists
Sorting by multiple criteria (name, artist, genre)
Recently played songs tracking
Full REST API implementation with Flask


Design Decisions:

Used a doubly linked list for the playlist to allow efficient insertion/removal at both ends
Maintained a hash table for O(1) song lookups while still preserving order with the linked list
Implemented a queue for recently played songs with a fixed size
Used QuickSort for sorting as it performs well in practice and has good average-case complexity

Getting Started
Dependencies
There is a txt file that includes all the dependencies that will be needed into a txt file for an easy install.
In the terminal you can perform a pip intall to install all dependencies in an easy manner.
The command is as follows:
pip install -r dependencies.txt

After that you can just press the run button on the main.py file or inside the console type:
python main.py 

That will start the flask app and lastly there is a test.py file with some test cases demonstrating how the app works.
Using postman is also an option but not necessary.

