# Play Video in the terminal
Playing any Video in the terminal using OpenCV and Pillow, a very simple and kinda scuffed way to do it.
It started off as trying to play Bad Apple in the terminal but ended as supporting almost any video


# Play
- To execute the program, use
### Linux
```bash
python3 play_video.py <path> <gradient>
```
### Windows
```shell
python play_video.py <path> <gradient>
```

## Arguments
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


# Dependencies
- OpenCV
- Pillow
- Numpy

### Install them with
```
pip install opencv-python pillow numpy
```