import math
import spotipy
from spotipy.oauth2 import SpotifyOAuth
    
# user variables
username = input("Enter your Spotify username:\n")
userID = input("Enter your Spotify user ID:\n")
clientID = input("Enter your Spotify client ID:\n")
clientSecret = input("Enter your Spotify secret client ID:\n")
playlistURL = input("All user information has been gathered. Enter the URL of the playlist you want to sort:\n")

print("Processing...")

# authorization variables
redirectURI = 'http://127.0.0.1:8080'
scope = 'playlist-modify-private','playlist-modify-public'
token = SpotifyOAuth(clientID,clientSecret,redirectURI,scope=scope,username=username)
sp = spotipy.Spotify(auth_manager = token)

# getting the playlist and its full length
playlist = sp.playlist(playlistURL)
results = playlist['tracks']
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
length = len(tracks)

# user chooses what characteristic to the playlist sort by
attribute = input("What attribute do you want to sort your new playlist by? The Spotify API allows these choices:\nrelease_date\n"+
        "popularity\ndanceability\nenergy\nkey\nloudness\nmode\nspeechiness\nacousticness\ninstrumentalness\nliveness\nvalence\ntempo\nduration_ms\ntime_signature\n")

# user determines whether attribute is sorted from greatest to least or vice versa
order = input("Do you want the songs in the playlist to be ordered by this attribute from greatest to least or least to greatest? Enter 'least' for least to greatest and vice versa.\n")
sortingOrder = True
if order == "least":
    sortingOrder = False
    
print("Processing...")

# for matching songs with their attributes and URLs
attributeDict = dict()
urlDict = dict()

# iterating through each track of the playlist and adding them to the dictionaries along with their characteristics
for i in range(length):
    track = playlist['tracks']['items'][i]['track']['external_urls']['spotify']
    url = playlist['tracks']['items'][i]['track']['external_urls']['spotify']
    if attribute == 'popularity':
        attributeAmount = playlist['tracks']['items'][i]['track']['popularity']
    elif attribute == 'release_date':
        attributeAmount = playlist['tracks']['items'][i]['track']['album']['release_date']
    else:
        attributeAmount = sp.audio_features(track)[0][attribute]
    artist = playlist['tracks']['items'][i]['track']['album']['artists'][0]['name']
    song = playlist['tracks']['items'][i]['track']['name']
    songString = artist + " - " + song
    attributeDict.update({songString : attributeAmount})
    urlDict.update({songString : url})

# this is the length of the original playlist when duplicate songs are excluded
length = len(urlDict.items())

# sorting the list by the attribute and to the user's preference
sortedList = list(dict(sorted(attributeDict.items(),reverse=sortingOrder,key=lambda x:x[1])))
urlList = []
for i in range(length):
    urlList.append(urlDict.get(sortedList[i]))

# user gets to enter certain information about the playlist
newName = input("Enter the new playlist's name:\n")
description = input("Enter the new playlist's description:\n")

print("Processing...")

# playlist is created
newPlaylist = sp.user_playlist_create(userID,newName,description=description)

# adding 100 songs at a time (the limit for a request) to the playlist from the sorted list of URLs
for i in range(math.ceil(length/100)):
    subList = []
    if (length - i*100 >= 100):
        for j in range(100):
            subList.append(urlList[i*100+j])
    else:
        for j in range(length - i*100):
            subList.append(urlList[i*100+j])
    sp.user_playlist_add_tracks(userID,newPlaylist['id'],subList)
    
# confirmation message and new playlist URL
print("The playlist has been successfully made! Check Spotify to see your new playlist or get it at this link:\n" + newPlaylist['external_urls']['spotify'])
