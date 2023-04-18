import pylast
from pick import pick
import os
import rich
from datetime import datetime
import json
from io import TextIOWrapper
from typing import List

def load_or_create_json()->None:
    if os.path.exists("albums.json"):
        with open("albums.json", "r") as f:
            ratings = json.load(f)
    else:
        # create a new json file with empty dict
        with open("albums.json", "w") as f:
            ratings = {"album_ratings":[], "song_ratings":[]}
            json.dump(ratings, f)
    
def get_album_list(artist: str)->List[str]:
    # GET THE TOP ALBUMS OF THE ARTIST AND STORE THEM IN A LIST
    artist = network.get_artist(artist)
    top_albums = artist.get_top_albums()
    album_list = [str(album.item) for album in top_albums]

    # CLEANUP THE LIST
    for album in album_list:
        if "(null)" in album:
            album_list.remove(album)

    # SORT THE LIST
    album_list.sort()

    # ADD EXIT OPTION
    album_list.insert(0, "EXIT")
    return album_list

        
def rate_by_album():
    load_or_create_json()
    with open("albums.json", "r") as f:
        album_file = json.load(f)
    print("RATE BY ARTIST")
    artist_search = input("Search for an artist: ")

    try:
        album_list = get_album_list(artist_search)
        
        # PICK THE ALBUMS
        print("Select albums to rate")
        while True:
            selected_album, index = pick(album_list, "Albums", indicator='→')
            if selected_album == 'EXIT':
                break

            artist, album = selected_album.split(" - ")
            rate_question = f"What's your rating for {album}?"
            options = ["★", "★"*2, "★"*3, "★"*4, "★"*5, "★"*6, "★"*7, "★"*8, "★"*9, "★"*10]
            rating, index = pick(options, rate_question, indicator='→')
            rating_time = datetime.now()

            # prompt for review
            review_question = f"Would you like to write a review for {album}?"
            review_options = ["Yes", "No"]
            review_choice, _ = pick(review_options, review_question, indicator='→')
            review = input("Write your review: ") if review_choice == "Yes" else ""
            
            # ! check if the album is already in the json file by looping through the "album_ratings" list
            album_found = False
            for collection in album_file["album_ratings"]:
                if collection["album"] == album:
                    # update the rating, time
                    collection["album_rating"] = index+1
                    collection["time"] = str(rating_time)
                    
                    # if current review is not empty, update the review with the new one otherwise keep the old one
                    if review != "":
                        collection["review"] = review
                    
                    album_found = True
                    print(f"You updated {artist}'s {album} to {rating} stars | {index+1}/10 | REVIEW: {review}")
                    break


            # ! if the album is not found, get the cover art and add new entry to the json file
            if not album_found:
                # get the cover art
                cover_art = network.get_album(artist, album).get_cover_image()

                # write to json file inside the "album_ratings" list
                album_file["album_ratings"].append({"artist":artist, "album": album, "cover": cover_art, "album_rating": index+1, "review": review, "time": str(rating_time), "track_ratings":[]})

                print(f"You gave {artist}'s {album} {rating} stars | {index+1}/10 | REVIEW: {review}")

        with open("albums.json", "w") as f:
            json.dump(album_file, f)


    except pylast.PyLastError:
        print("Artist not found")
 
def rate_album_songs():
    load_or_create_json()
    with open("albums.json", "r") as f:
        album_file = json.load(f)
    
    # show all albums from the file
    albums_in_file = []
    for collection in album_file["album_ratings"]:
        artist_temp = collection["artist"]
        album_temp = collection["album"]
        albums_in_file.append(f"{artist_temp} - {album_temp}")
    
    
    albums_in_file.sort() 
    albums_in_file.insert(0, "EXIT")
    
    # if there are no albums in the file based on the artist, exit
    if not len(albums_in_file):
        print("No albums found")
        return

    # pick an album to rate
    selected_album, index = pick(albums_in_file, "Albums", indicator='→')
    if selected_album == "EXIT":
        return
    
    artist, album = selected_album.split(" - ")
    # get the tracks from the album
    tracks = network.get_album(artist, album).get_tracks()
    tracks = [track.title for track in tracks]
    tracks.insert(0, "EXIT")

    while True:
        selected_track, index = pick(tracks, "Tracks", indicator='→')
        if selected_track == "EXIT":
            break
        
        # get the rating
        rate_question = f"What's your rating for {selected_track}?"
        options = ["★", "★"*2, "★"*3, "★"*4, "★"*5, "★"*6, "★"*7, "★"*8, "★"*9, "★"*10]
        rating, index = pick(options, rate_question, indicator='→')
        
        # check if the track is already in the json file
        track_found = False
        for collection in album_file["album_ratings"]:
            if collection["album"] == album:
                for track in collection["track_ratings"]:
                    if track["track"] == selected_track:
                        track["track_rating"] = index+1
                        track_found = True
                        print(f"You updated {artist}'s {selected_track} to {rating} stars | {index+1}/10")
                        break
                break   
                
        
        # if the track is not found, add it to the json file
        if not track_found:
            # go into the album and add the track
            for collection in album_file["album_ratings"]:
                if collection["album"] == album:
                    collection["track_ratings"].append({"track": selected_track, "track_rating": index+1})
                    print(f"You gave {artist}'s {selected_track} {rating} stars | {index+1}/10")
                    break
        with open("albums.json", "w") as f:
            json.dump(album_file, f)
    

def rate_single_song():
    load_or_create_json()
    with open("albums.json", "r") as f:
        album_file = json.load(f)
    
     
    song_input = input("What's the name of the song?\t")
    artist_input = input("What's the name of the artist?\t")
    
    
    # validate the song
    track = network.search_for_track(artist_input, song_input)
    results = track.get_next_page()
    
    if not results:
        print("Song not found")
        return
    
    song = results[0]
    rate_question = f"What's your rating for {song.title}?"
    options = ["★", "★"*2, "★"*3, "★"*4, "★"*5, "★"*6, "★"*7, "★"*8, "★"*9, "★"*10]
    rating, index = pick(options, rate_question, indicator='→')
    # check if the track is already in the json file
    track_found = False
    for collection in album_file["song_ratings"]:
        if collection["track"] == song.title:
            collection["track_rating"] = index+1
            track_found = True
            print(f"You updated {song.artist.name}'s {song.title} to {rating} stars | {index+1}/10")
            break
    
    # if the track is not found, add it to the json file
    if not track_found: 
        album_file["song_ratings"].append({"track": song.title, "artist":song.artist.name, "track_rating": index+1})
        print(f"You gave {song.artist.name}'s {song.title} {rating} stars | {index+1}/10")
            
    with open("albums.json", "w") as f:
        json.dump(album_file, f)
    
    
def rate_by_song():
    question = "What do you want to do?"
    options = ['Rate All Songs From an Album', 'Rate a Single Song']
    selected_option, index = pick(options, question, indicator='→')
    if index == 0:
        rate_album_songs()
    elif index == 1:
        rate_single_song()            
                
if __name__ == "__main__":
    LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
    LASTFM_API_SECRET = os.environ.get("LASTFM_API_SECRET")
    startup_question = "What do you want to do?"
    options = ['Rate by Album', 'Rate Songs']
    selected_option, index = pick(options, startup_question, indicator='→')
    network = pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET)
    
    if index == 0:
        rate_by_album()
    elif index == 1:
        rate_by_song()
        
    
     
# - Rate by Artist -> Search Artist -> Show Artist Albums and allow selection -> once selected ask for a rating on a 10 point scale -> save the date, rating, album -> Show the tracks and optionally prompt to rate each track [Y/N] -> 