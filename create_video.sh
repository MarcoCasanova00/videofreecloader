ffmpeg -framerate 1 -i encoded_pages/page_%03d.png -vf "setpts=1.0*5/(1.0*1),fps=1" -c:v libx264 -r 1 output.mp4