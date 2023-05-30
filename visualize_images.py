import requests
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO
import time

def plot_images_with_rectangles(file_path):
    with open(file_path) as file:
        data = json.load(file)

    for item in data:
        image_url = item['thumbnails_webimage']
        print(image_url)
        #print(item['property_product_coordinates'])
        coordinates = json.loads('[' + item['property_product_coordinates'] + ']')
        name = item["name"]

        try:
            response = requests.get(image_url, stream=True)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image = image.convert('RGB')
        except Exception as e:
            print("Error loading image:", e)
            time.sleep(1)  # Wait for 1 second before retrying
            print("sleeping 1")

        fig, ax = plt.subplots()
        ax.imshow(image)

        for coord in coordinates:
            box = coord['box']
            dot = coord['dot']

            left = float(box['l']) * image.width
            top = float(box['t']) * image.height
            width = float(box['w']) * image.width
            height = float(box['h']) * image.height

            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

            dot_x = float(dot['x']) * image.width
            dot_y = float(dot['y']) * image.height

            ax.plot(dot_x, dot_y, 'ro')

        plt.savefig(f"figures/raw_bounding_boxes/{name}.png")
        print(f"Saved figure figures/raw_bounding_boxes/{name}.png")

if __name__ == "__main__":
    # Load the contents of JSON
    json_file = 'DATA/filtered_data_mt3_prob_clean.json'      
    plot_images_with_rectangles(json_file)
