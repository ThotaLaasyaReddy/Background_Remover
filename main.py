from rembg import remove
from PIL import Image
import sys
if len(sys.argv) != 3:
    print("Usage: python main.py <input_path> <output_path>")
    sys.exit(1)
input_path = sys.argv[1]
output_path = sys.argv[2]
try:
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)
    print(f"Processed image saved at {output_path}")
except Exception as e:
    print(f"Error processing image: {e}")
    sys.exit(1)
