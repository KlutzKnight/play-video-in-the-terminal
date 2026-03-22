# bad-apple-in-the-terminal
Playing Bad Apple in the terminal using OpenCV and Pillow, a very simple and scuffed way to do it

# Play
- To execute, run the code
```
python play_video.py <path> <gradient>
```
### path
    - full or relative path of the video file
### gradient
    - grayscale gradient
    - use 2 for black and white, 10 otherwise

# How it works
- Extract the frame by frame data of .mp4 video
- Convert to grayscale and resize to fit the terminal
- Normalize the values from [0, 255] to the given parameters
- Save the Video frames to txt file
- Play the video from the txt file