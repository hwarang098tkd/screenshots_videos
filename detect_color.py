import os
from colorthief import ColorThief
from sklearn.cluster import KMeans
from collections import Counter

def detect_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def search_and_detect_color(folder_path):
    counter = 1

    for filename in os.listdir(folder_path):
        if "DET" in filename:
            image_path = os.path.join(folder_path, filename)
            dominant_color = detect_dominant_color(image_path)
            color_name = get_color_name(dominant_color)

            new_filename = f"DET_{counter}.jpg"
            new_image_path = os.path.join(folder_path, new_filename)
            #os.rename(image_path, new_image_path)

            print(f"Image: {filename} - Dominant Color: {color_name} {dominant_color}")
            counter += 1


def get_color_name(color):
    colors = {
        (0, 0, 255): "blue",
        (0, 255, 0): "green",
        (255, 0, 0): "red",
        (255, 255, 255): "white",
        (0, 0, 0): "black"
        # Add more colors as needed
    }

    for predefined_color, color_name in colors.items():
        if color_distance(predefined_color, color) <= 20:
            return color_name

    return "unknown"

def color_distance(color1, color2):
    return sum(abs(c1 - c2) for c1, c2 in zip(color1, color2))

# Provide the folder path where the images are located
folder_path = 'C:\\Users\\hwa_r\\output_hiv00000.mp4'

# Search for DET images and detect the dominant color in each image
search_and_detect_color(folder_path)
