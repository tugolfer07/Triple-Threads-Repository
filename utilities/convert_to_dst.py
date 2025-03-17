import numpy as np
from PIL import Image
from pyembroidery import EmbPattern, write_dst

def image_to_dst(image_path, output_path):
    try:
        print(f"🟡 Attempting to open image: {image_path}")

        # Open image and convert to grayscale
        image = Image.open(image_path).convert("L")
        image = image.resize((200, 200))  # Resize for embroidery machine compatibility
        img_array = np.array(image, dtype=np.uint8)  # Ensure 8-bit integer format

        print(f"✅ Image successfully loaded and converted to grayscale.")

        # Create an embroidery pattern
        pattern = EmbPattern()

        # Convert image pixels into embroidery stitches
        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                if int(img_array[y, x]) & 128:  # Ensure it's an integer before bitwise AND
                    # Ensure the X, Y coordinates are integers
                    x_int, y_int = int(x), int(y)
                    pattern.add_stitch_absolute("STITCH", x_int, y_int)

        print(f"✅ Embroidery pattern created successfully.")

        # 🛠 Debugging: Check if any stitches exist before writing
        print(f"🛠 Pattern Stitch Count: {len(pattern.stitches)}")
        if len(pattern.stitches) > 0:
            print(f"🛠 First 5 Stitches: {pattern.stitches[:5]}")  # Show first few stitches

        # Ensure all stitch data is properly formatted as integers before writing
        print(f"🟡 Saving DST file: {output_path}")

        # 🛠 Final Stitch Data Type Check
        for i, stitch in enumerate(pattern.stitches[:5]):  # Check first 5
            print(f"🛠 Stitch {i}: {stitch} | Types: {[type(s) for s in stitch]}")

        with open(output_path, "wb") as dst_file:
            write_dst(pattern, dst_file)

        print(f"✅ DST file saved successfully: {output_path}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

# Run script (Make sure the path is correct)
image_to_dst("C:/Users/Owner/triple-threads-repository/utilities/example.png",
             "C:/Users/Owner/triple-threads-repository/utilities/output.dst")