import requests
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import json

def image_generator(file_name, data):

    # return if the file already exists
    if os.path.exists(file_name):
        return
    
    # Set the image size and font
    image_width = 1920
    image_height = 5000
    font = ImageFont.truetype("arial.ttf", 15)
    tier_font = ImageFont.truetype("arial.ttf", 30)
    # Make a new image with the size and background color black
    image = Image.new("RGB", (image_width, image_height), "black")
    text_cutoff_value = 20

    #Initialize variables for row and column positions
    row_pos = 0
    col_pos = 0
    increment_size = 200
    
    for count, album in enumerate(data["s_tier"]):
        # leftmost side - make a square with text inside the square and fill color green
        if col_pos == 0:
            draw = ImageDraw.Draw(image)
            draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="red")
            draw.text((col_pos + (increment_size//3), row_pos + (increment_size//3)), "S Tier", font=tier_font, fill="white")
            col_pos += increment_size

        # Get the cover art
        # check if the cover art is not None
        if album["cover_art"] is not None: 
            response = requests.get(album["cover_art"])
        else:
            response = requests.get("https://i.imgur.com/0YK1Z2L.png")
        cover_art = Image.open(BytesIO(response.content))
        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0

    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0

    """A TIER"""
    # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="orange")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "A Tier", font=tier_font, fill="white")
        col_pos += increment_size
        
    for album in data["a_tier"]:
        # Get the cover art
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0 

    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0
    
    """B TIER"""
    # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="yellow")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "B Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for album in data["b_tier"]:
        # Get the cover art
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0
    
    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0
    
    """C TIER"""
        # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="green")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "C Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for album in data["c_tier"]:
        # Get the cover art
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0
    
    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0
   

    """D TIER"""
    # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="blue")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "D Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for album in data["d_tier"]:
        # Get the cover art
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0
    
    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0


    """E TIER"""
        # leftmost side - make a square with text inside the square and fill color
    if col_pos == 0:
        draw = ImageDraw.Draw(image)
        draw.rectangle((col_pos, row_pos, col_pos + increment_size, row_pos + increment_size), fill="pink")
        draw.text((col_pos + (increment_size//3), row_pos+(increment_size//3)), "E Tier", font=tier_font, fill="black")
        col_pos += increment_size
        
    for album in data["e_tier"]:
        # Get the cover art
        response = requests.get(album["cover_art"])
        cover_art = Image.open(BytesIO(response.content))
        # Resize the cover art
        cover_art = cover_art.resize((increment_size, increment_size))
        # Paste the cover art onto the base image
        image.paste(cover_art, (col_pos, row_pos))
        # Draw the album name on the image with the font size 10 and background color white
        draw = ImageDraw.Draw(image)

        # Get the album name
        name = album["album"]
        if len(name) > text_cutoff_value:
            name = f"{name[:text_cutoff_value]}..."

        draw.text((col_pos, row_pos + increment_size), name, font=font, fill="white")

        # Increment the column position
        col_pos += 200
        # check if the column position is greater than the image width
        if col_pos > image_width - increment_size:
            # add a new row
            row_pos += increment_size + 50
            col_pos = 0
    
    # add a new row to separate the tiers
    row_pos += increment_size + 50
    col_pos = 0
    
    # crop the image to trim the extra space below the last row
    image = image.crop((0, 0, image_width, row_pos))

    # save the image two directories up
    image.save(f"{file_name}")
    
