import json
import os
from datetime import datetime
from typing import List

import pylast
from pick import pick

from rich import print
from rich.table import Table

import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from tiermaker import image_generator

def load_or_create_json() -> None:
    if os.path.exists("albums.json"):
        with open("albums.json") as f:
            ratings = json.load(f)
    else:
        # create a new json file with empty dict
        with open("albums.json", "w") as f:
            ratings = {"album_ratings": [], "song_ratings": [], "tier_lists": []}
            json.dump(ratings, f)


def get_album_list(artist: str) -> List[str]:
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


def rate_by_album() -> None:
    load_or_create_json()
    with open("albums.json") as f:
        album_file = json.load(f)
    print("RATE BY ARTIST")
    artist_search = input("Search for an artist: ")

    try:
        album_list = get_album_list(artist_search)

        # PICK THE ALBUMS
        print("Select albums to rate")
        while True:
            selected_album, index = pick(album_list, "Albums", indicator="→")
            if selected_album == "EXIT":
                break

            artist, album = selected_album.split(" - ", maxsplit=1)
            rate_question = f"What's your rating for {album}?"
            options = [
                "★",
                "★" * 2,
                "★" * 3,
                "★" * 4,
                "★" * 5,
                "★" * 6,
                "★" * 7,
                "★" * 8,
                "★" * 9,
                "★" * 10,
            ]
            rating, index = pick(options, rate_question, indicator="→")
            rating_time = datetime.now()

            # prompt for review
            review_question = f"Would you like to write a review for {album}?"
            review_options = ["Yes", "No"]
            review_choice, _ = pick(review_options, review_question, indicator="→")
            review = input("Write your review: ") if review_choice == "Yes" else ""

            # ! check if the album is already in the json file by looping through the "album_ratings" list
            album_found = False
            for collection in album_file["album_ratings"]:
                if collection["album"] == album:
                    # update the rating, time
                    collection["album_rating"] = index + 1
                    collection["time"] = str(rating_time)

                    # if current review is not empty, update the review with the new one otherwise keep the old one
                    if review != "":
                        collection["review"] = review

                    album_found = True
                    print(
                        f"You updated {artist}'s {album} to {rating} stars | {index+1}/10 | REVIEW: {review}"
                    )
                    break

            # ! if the album is not found, get the cover art and add new entry to the json file
            if not album_found:
                # get the cover art
                cover_art = network.get_album(artist, album).get_cover_image()

                # write to json file inside the "album_ratings" list
                album_file["album_ratings"].append(
                    {
                        "artist": artist,
                        "album": album,
                        "cover": cover_art,
                        "album_rating": index + 1,
                        "review": review,
                        "time": str(rating_time),
                        "track_ratings": [],
                    }
                )

                print(
                    f"You gave {artist}'s {album} {rating} stars | {index+1}/10 | REVIEW: {review}"
                )

        with open("albums.json", "w") as f:
            json.dump(album_file, f)

    except pylast.PyLastError:
        print("Artist not found")


def rate_album_songs():
    load_or_create_json()
    with open("albums.json") as f:
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
    selected_album, index = pick(albums_in_file, "Albums", indicator="→")
    if selected_album == "EXIT":
        return

    artist, album = selected_album.split(" - ", maxsplit=1)
    # get the tracks from the album
    tracks = network.get_album(artist, album).get_tracks()
    tracks = [track.title for track in tracks]
    tracks.insert(0, "EXIT")

    while True:
        selected_track, index = pick(tracks, "Tracks", indicator="→")
        if selected_track == "EXIT":
            break

        # get the rating
        rate_question = f"What's your rating for {selected_track}?"
        options = [
            "★",
            "★" * 2,
            "★" * 3,
            "★" * 4,
            "★" * 5,
            "★" * 6,
            "★" * 7,
            "★" * 8,
            "★" * 9,
            "★" * 10,
        ]
        rating, index = pick(options, rate_question, indicator="→")

        # check if the track is already in the json file
        track_found = False
        for collection in album_file["album_ratings"]:
            if collection["album"] == album:
                for track in collection["track_ratings"]:
                    if track["track"] == selected_track:
                        track["track_rating"] = index + 1
                        track_found = True
                        print(
                            f"You updated {artist}'s {selected_track} to {rating} stars | {index+1}/10"
                        )
                        break
                break

        # if the track is not found, add it to the json file
        if not track_found:
            # go into the album and add the track
            for collection in album_file["album_ratings"]:
                if collection["album"] == album:
                    collection["track_ratings"].append(
                        {"track": selected_track, "track_rating": index + 1}
                    )
                    print(
                        f"You gave {artist}'s {selected_track} {rating} stars | {index+1}/10"
                    )
                    break
        with open("albums.json", "w") as f:
            json.dump(album_file, f)


def rate_single_song():
    load_or_create_json()
    with open("albums.json") as f:
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
    options = [
        "★",
        "★" * 2,
        "★" * 3,
        "★" * 4,
        "★" * 5,
        "★" * 6,
        "★" * 7,
        "★" * 8,
        "★" * 9,
        "★" * 10,
    ]
    rating, index = pick(options, rate_question, indicator="→")
    # check if the track is already in the json file
    track_found = False
    for collection in album_file["song_ratings"]:
        if collection["track"] == song.title:
            collection["track_rating"] = index + 1
            track_found = True
            print(
                f"You updated {song.artist.name}'s {song.title} to {rating} stars | {index+1}/10"
            )
            break

    # if the track is not found, add it to the json file
    if not track_found:
        album_file["song_ratings"].append(
            {"track": song.title, "artist": song.artist.name, "track_rating": index + 1}
        )
        print(
            f"You gave {song.artist.name}'s {song.title} {rating} stars | {index+1}/10"
        )

    with open("albums.json", "w") as f:
        json.dump(album_file, f)


def rate_by_song():
    question = "What do you want to do?"
    options = ["Rate All Songs From an Album", "Rate a Single Song"]
    selected_option, index = pick(options, question, indicator="→")
    if index == 0:
        rate_album_songs()
    elif index == 1:
        rate_single_song()


def see_albums_rated():
    load_or_create_json()
    with open("albums.json") as f:
        album_file = json.load(f)

    # sort alphabetically
    album_file["album_ratings"].sort(key=lambda x: x["album"])

    # add a rich table
    table = Table(title="Album Ratings")
    table.add_column("Artist", justify="left", style="cyan")
    table.add_column("Album", justify="left", style="cyan")
    table.add_column("Rating", justify="left", style="cyan")
    table.add_column("Time", justify="left", style="cyan")


    for collection in album_file["album_ratings"]:
        artist = collection["artist"]
        album = collection["album"]
        rating = str(collection["album_rating"])

        # convert to human readable time
        time = collection["time"]
        time = time.split(" ")[0]
        time = datetime.strptime(time, "%Y-%m-%d").strftime("%b %d, %Y")

        # add the row
        table.add_row(artist, album, rating, time)

    print(table)
    return

def see_songs_rated():
    load_or_create_json()
    with open("albums.json") as f:
        album_file = json.load(f)

    # SONGS - SINGLE SONGS

    # sort alphabetically
    album_file["song_ratings"].sort(key=lambda x: x["track"])

    # add a rich table
    table = Table(title="Song Ratings - Singles")
    table.add_column("Artist", justify="left", style="cyan")
    table.add_column("Song", justify="left", style="cyan")
    table.add_column("Rating", justify="left", style="cyan")


    for collection in album_file["song_ratings"]:
        artist = collection["artist"]
        song = collection["track"]
        rating = str(collection["track_rating"])

        # add the row
        table.add_row(artist, song, rating)

    print(table)

    # SONGS - ALBUMS

    # sort alphabetically
    album_file["album_ratings"].sort(key=lambda x: x["album"])

    # add a rich table
    table = Table(title="Song Ratings - From Albums")
    table.add_column("Artist", justify="left", style="cyan")
    table.add_column("Album", justify="left", style="cyan")
    table.add_column("Track", justify="left", style="cyan")
    table.add_column("Rating", justify="left", style="cyan")

    for collection in album_file["album_ratings"]:
        artist = collection["artist"]
        album = collection["album"]
        rating = str(collection["album_rating"])
        for track in collection["track_ratings"]:
            track_name = track["track"]
            table.add_row(artist, album, track_name, rating)

    print(table)
    return


def create_tier_list_helper(albums_to_rank, tier_name):
    # if there are no more albums to rank, return an empty list
    if not albums_to_rank:
        return []
    
    question = f"Select the albums you want to rank in  {tier_name}"
    tier_picks = pick(options=albums_to_rank, title=question, multiselect=True, indicator="→", min_selection_count=0)
    tier_picks = [x[0] for x in tier_picks]
    
    for album in tier_picks:
        albums_to_rank.remove(album)

    return tier_picks


def get_album_cover(artist, album):
    album = network.get_album(artist, album)
    album_cover = album.get_cover_image()
    return album_cover

def create_tier_list():
    load_or_create_json()
    with open("albums.json") as f:
        album_file = json.load(f)

    print("TIERS - S, A, B, C, D, E")

    question = "Which artist do you want to make a tier list for?"
    artist = input(question).strip().lower()
    
    try:
        get_artist = network.get_artist(artist)
        artist = get_artist.get_name()
        albums_to_rank = get_album_list(artist)
        
        # keep only the album name by splitting the string at the first - and removing the first element
        albums_to_rank = [x.split(" - ", 1)[1] for x in albums_to_rank[1:]]

        question = "What do you want to call this tier list?"
        tier_list_name = input(question).strip()

        # S TIER
        question = "Select the albums you want to rank in S Tier:"
        s_tier_picks = create_tier_list_helper(albums_to_rank, "S Tier")
        s_tier_covers = [get_album_cover(artist, album) for album in s_tier_picks]
        s_tier = [{"album":album,"cover_art": cover} for album, cover in zip(s_tier_picks, s_tier_covers)]
        
        # A TIER
        question = "Select the albums you want to rank in A Tier:"
        a_tier_picks = create_tier_list_helper(albums_to_rank, "A Tier")
        a_tier_covers = [get_album_cover(artist, album) for album in a_tier_picks]
        a_tier = [{"album":album,"cover_art": cover} for album, cover in zip(a_tier_picks, a_tier_covers)]
            
        # B TIER
        question = "Select the albums you want to rank in B Tier:"
        b_tier_picks = create_tier_list_helper(albums_to_rank, "B Tier")
        b_tier_covers = [get_album_cover(artist, album) for album in b_tier_picks]
        b_tier = [{"album":album,"cover_art": cover} for album, cover in zip(b_tier_picks, b_tier_covers)]
        
        # C TIER
        question = "Select the albums you want to rank in C Tier:"
        c_tier_picks = create_tier_list_helper(albums_to_rank, "C Tier")
        c_tier_covers = [get_album_cover(artist, album) for album in c_tier_picks]
        c_tier = [{"album":album,"cover_art": cover} for album, cover in zip(c_tier_picks, c_tier_covers)]
            
        # D TIER
        question = "Select the albums you want to rank in D Tier:"
        d_tier_picks = create_tier_list_helper(albums_to_rank, "D Tier")
        d_tier_covers = [get_album_cover(artist, album) for album in d_tier_picks] 
        d_tier = [{"album":album,"cover_art": cover} for album, cover in zip(d_tier_picks, d_tier_covers)]
            
        
        # E TIER
        question = "Select the albums you want to rank in E Tier:"
        e_tier_picks = create_tier_list_helper(albums_to_rank, "E Tier")
        e_tier_covers = [get_album_cover(artist, album) for album in e_tier_picks]
        e_tier = [{"album":album,"cover_art": cover} for album, cover in zip(e_tier_picks, e_tier_covers)]
        
        # check if all tiers are empty and if so, exit
        if not any([s_tier_picks, a_tier_picks, b_tier_picks, c_tier_picks, d_tier_picks, e_tier_picks]):
            print("All tiers are empty. Exiting...")
            return
        
        
        # # add the albums that were picked to the tier list
        tier_list = {
            "tier_list_name": tier_list_name,
            "artist": artist,
            "s_tier": s_tier, 
            "a_tier": a_tier,
            "b_tier": b_tier,
            "c_tier": c_tier,
            "d_tier": d_tier,
            "e_tier": e_tier,
            "time": str(datetime.now())
        }
        
        # add the tier list to the json file
        album_file["tier_lists"].append(tier_list)
        
        # save the json file
        with open("albums.json", "w") as f:
            json.dump(album_file, f, indent=4)
            
        return
    
    except pylast.PyLastError:
        print("Artist not found")

def see_tier_lists():
    load_or_create_json()
    with open("albums.json", "r") as f:
        data = json.load(f)

    if not data["tier_lists"]:
        print("No tier lists created yet! Make one first!")
        return
    
    for key in data["tier_lists"]:
        image_generator(f"{key['tier_list_name']}.png", key)
        print(f"Generated {key['tier_list_name']}.png")
        
    print("Done! Created all tier lists!")    


LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
LASTFM_API_SECRET = os.environ.get("LASTFM_API_SECRET")
network = pylast.LastFMNetwork(api_key=LASTFM_API_KEY, api_secret=LASTFM_API_SECRET)

def start():    
    global network
    
    startup_question = "What do you want to do?"
    options = ["Rate by Album", "Rate Songs", "See Albums Rated", "See Songs Rated", "Make a Tier List", "See Created Tier Lists", "EXIT"]
    selected_option, index = pick(options, startup_question, indicator="→")
    
    if index == 0:
        rate_by_album()
    elif index == 1:
        rate_by_song()
    elif index == 2:
        see_albums_rated()
    elif index == 3:
        see_songs_rated()
    elif index == 4:
        create_tier_list()
    elif index == 5:
        see_tier_lists()
    elif index == 6:
        exit()

start()
