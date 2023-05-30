import requests
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO
import time

def plot_image_with_boxes_and_dots(image_path, box_parameters, name):
    # Convert box_parameters from string to a list of dictionaries

    if isinstance(image_path, str) and os.path.isfile(image_path):
        # Read image from local file
        image = Image.open(image_path).convert('RGB')
    else:
        # Read image from web link
        with urllib.request.urlopen(image_path) as response:
            image_data = response.read()
        # Convert image data to PIL Image object
        image = Image.open(BytesIO(image_data))

    # Get image width and height
    image_width, image_height = image.size

    # Create a figure and axis
    fig, ax = plt.subplots()

    # Display the image
    ax.imshow(image)

    print("json loads", box_parameters)
    # Process each box parameter
    for box_param in box_parameters:
        # Extract box coordinates
        box_left = float(box_param['box']['l'])
        box_top = float(box_param['box']['t'])
        box_width = float(box_param['box']['w'])
        box_height = float(box_param['box']['h'])

        # Calculate box coordinates in the plot
        x = box_left * image_width
        y = box_top * image_height
        w = box_width * image_width
        h = box_height * image_height

        # Create a rectangle patch
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')

        # Add the rectangle patch to the plot
        ax.add_patch(rect)

        # Extract dot coordinates
        dot_x = float(box_param['dot']['x'])
        dot_y = float(box_param['dot']['y'])

        # Calculate dot coordinates in the plot
        dot_x_plot = dot_x * image_width
        dot_y_plot = dot_y * image_height

        # Plot the dot
        ax.plot(dot_x_plot, dot_y_plot, 'bo', markersize=5)

    # Set axis limits
    ax.set_xlim(0, image_width)
    ax.set_ylim(image_height, 0)

    # Show the plot
    plt.savefig(f"figures/raw_bounding_boxes/{name}.png")
    print(f"Saved figure figures/raw_bounding_boxes/{name}.png")


def plot_images_with_rectangles(file_path):
    with open(file_path) as file:
        data = json.load(file)

    for item in data:
        image_url = item['thumbnails_webimage']
        print(image_url)
        print(item['property_product_coordinates'])
        coordinates = json.loads('[' + item['property_product_coordinates'] + ']')
        name = item["name"]

        #try:
        #    response = requests.get(image_url, stream=True)
        #    image = Image.open(BytesIO(response.content))
        #    image = image.convert('RGB')
        #except Exception as e:
        #    print("Error loading image:", e)
        #    time.sleep(1)  # Wait for 1 second before retrying
        #    print("Sleeping 1 sec")

        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        fig, ax = plt.subplots()
        ax.imshow(image)

        for coord in coordinates:
            print(coord)
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
