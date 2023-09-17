import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import pytesseract

# Step 1: Ask for a file
input_file = input("Enter the path to the file you want to encode: ")

# Step 2: Compress the file
compressed_file = input_file + '.zip'
subprocess.run(['zip', compressed_file, input_file])

# Step 3: Strip the extension and make it into text
text = os.path.splitext(compressed_file)[0]

# Step 4: Create images with the resulting text
output_folder = 'encoded_pages'
os.makedirs(output_folder, exist_ok=True)

# Set the frame rate and duration per frame (in seconds)
frame_rate = 1  # One frame per second
frame_duration = 5  # Display each page for 5 seconds

# Use a system font
font = ImageFont.load_default()  # Use the default system font

page_width, page_height = 800, 600
lines = [text[i:i+80] for i in range(0, len(text), 80)]  # Split text into lines

for i, page_text in enumerate(lines):
    image = Image.new('RGB', (page_width, page_height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Calculate text position
    text_x = 50
    text_y = 50
    line_height = 30
    
    # Write text to the image
    for line in page_text.split('\n'):
        draw.text((text_x, text_y), line, fill='black', font=font)
        text_y += line_height
    
    image.save(os.path.join(output_folder, f'page_{i + 1:03d}.png'))

# Step 5: Execute a bash script to turn pages into a video
with open('create_video.sh', 'w') as f:
    f.write(f'ffmpeg -framerate {frame_rate} -i {output_folder}/page_%03d.png -vf "setpts=1.0*{frame_duration}/(1.0*{frame_rate}),fps={frame_rate}" -c:v libx264 -r {frame_rate} output.mp4')

subprocess.run(['bash', 'create_video.sh'])

