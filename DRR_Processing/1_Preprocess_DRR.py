import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import time

def enhance_contrast(image_path, brightness=0, contrast=1):
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Enhance contrast
    enhanced_image = cv2.addWeighted(image, contrast, np.zeros(image.shape, image.dtype), 0, brightness)
    return enhanced_image
 
def crop_image(image):
    # Convert the image to a PIL Image for cropping
    im = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    immat = im.load()
    (X, Y) = im.size
    m = np.zeros((X, Y))

    # Create a brightness map
    for x in range(X):
        for y in range(Y):
            m[x, y] = immat[(x, y)] > (20,20,20 )
    m = m / np.sum(np.sum(m))

    # Marginal distributions
    dx = np.sum(m, axis=1)
    dy = np.sum(m, axis=0)

    # Expected values
    x = np.sum(dx * np.arange(X))
    y = np.sum(dy * np.arange(Y))

    # Cropping dimensions
    cx1 = int(x - 112)
    cy1 = int(y - 112)
    cx2 = cx1 + 224
    cy2 = cy1 + 224

    # Crop and return as a NumPy array
    crop = im.crop((cx1, cy1, cx2, cy2))
    return cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)

def expand_channels(img):
    # If the input image is grayscale, expand it to 3 channels
    if len(img.shape) == 2 or img.shape[2] == 1:
        expanded = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        expanded[:, :, 0] = img  # Red channel
        expanded[:, :, 1] = img  # Green channel
        expanded[:, :, 2] = img  # Blue channel
        return expanded
    return img  # Return the original image if it's already 3 channels

def threshold(img):
    threshold = np.array([8, 8, 8], dtype=np.uint8)
    mask = np.all(img < threshold, axis=-1)
    img[mask] = 0
    return img 

input_path = r"D:\drr475"
enhanced_output_dir = r"D:\drr475\enhanced"

# input_path = r"C:\Users\neera\Downloads\verse_DRR"
# enhanced_output_dir = r"C:\Users\neera\Downloads\verse_DRR\enhanced"

if not os.path.exists(enhanced_output_dir):
    os.makedirs(enhanced_output_dir)

start_time = time.time()
for filename in os.listdir(input_path):
    if filename.endswith(".png"):
        path = os.path.join(input_path, filename)
        output_path = os.path.join(enhanced_output_dir, filename)

        # Perform the 3 operations sequentially
        enhanced_img = enhance_contrast(path)       # Step 1: Enhance contrast
        cropped_img = crop_image(enhanced_img)     # Step 2: Crop the image
        #cropped_img = crop_image(path)
        expand_img = expand_channels(cropped_img)   # Step 3: Expand to 3 channels if needed
        final_img = threshold(expand_img)
        
        # Save the final image
        cv2.imwrite(output_path, expand_img)
end_time = time.time()
elapsed_time = end_time-start_time
print(f"Batch processing complete in {elapsed_time:.2f}")
