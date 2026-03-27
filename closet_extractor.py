from rembg import remove
from PIL import Image
import os

def extract_clothing(input_path, output_path):
    """
    Takes a photo of clothing, removes the background, 
    and saves it as a transparent PNG.
    """
    print(f"Processing: {input_path}...")
    
    try:
        # Load the original image
        input_image = Image.open(input_path)
        
        # Run the AI background removal
        output_image = remove(input_image)
        
        # Save the clean clothing item
        output_image.save(output_path)
        print(f"Success! Saved clean item to: {output_path}")
        
    except Exception as e:
        print(f"Oops, something went wrong: {e}")

# --- Let's test it! ---
if __name__ == "__main__":
    # Replace these with your actual file names
    my_messy_photo = "my_shirt.jpg" 
    my_clean_item = "clean_shirt.png"
    
    # Check if the file exists before running
    if os.path.exists(my_messy_photo):
        extract_clothing(my_messy_photo, my_clean_item)
    else:
        print(f"Please put a photo named '{my_messy_photo}' in the same folder as this script!")