import os
import subprocess
import pytesseract
import youtube_dl

# Step 1: Ask for a YouTube link
youtube_link = input("Enter the YouTube video link: ")

# Step 2: Download the video
output_video = 'downloaded_video.mp4'
ydl_opts = {
    'outtmpl': output_video,
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtube_link])

# Step 3: Make snapshots every X seconds
output_folder = 'decoded_pages'
os.makedirs(output_folder, exist_ok=True)
subprocess.run(['ffmpeg', '-i', output_video, '-vf', 'fps=1', f'{output_folder}/page_%03d.png'])

# Step 4: Perform OCR on the resulting snapshots
decoded_text = ''
for filename in sorted(os.listdir(output_folder)):
    image_path = os.path.join(output_folder, filename)
    text = pytesseract.image_to_string(Image.open(image_path))
    decoded_text += text

# Step 5: Create a file from the acquired text
decoded_file = 'decoded.txt'
with open(decoded_file, 'w') as f:
    f.write(decoded_text)

