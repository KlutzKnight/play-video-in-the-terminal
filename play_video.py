from PIL import Image
import cv2 as cv
import numpy as np
import time
import os
import sys
import shutil

def make_frames(in_path, out_path):
    """
    Makes the ascii art of each frame in video and saves it to out_path, normalizing it to [0, 9]

    @param in_path: the video to extract the frames
    @param out_path: the output path to store the ascii art

    returns: nothing
    """
    video = cv.VideoCapture(in_path)
    video_frames = []
    if video.isOpened():
        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = width / height

        terminal_size = shutil.get_terminal_size()
        terminal_height = terminal_size.lines - 1
        terminal_width = terminal_size.columns

        rendered_height = terminal_height
        rendered_width = min(terminal_width, int(rendered_height * aspect_ratio * 2))

    while video.isOpened():
        success, frame = video.read()

        # if frame is read correctly success is True
        if not success:
            print("Can't receive frame (stream end?). Saving...")
            break
        
        # Change to grayscale and resize
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        
        frame = Image.fromarray(frame).resize((rendered_width, rendered_height))

        # Make image an ndarray and normalize it to [0, 9]
        frame = np.asarray(frame)
        frame = normalize(frame)

        video_frames.append(frame)
    
    save_to_file(video_frames, out_path)
    video.release()


def normalize(matrix):
    """
    Normalized the matrix values from [0,255] to [0, 9] using min-max scaling

    @param matrix: Matrix of values ranging from [0, 255]

    returns: normalized matrix
    """
    normalization_factor = (10 - 1)/255
    return matrix * normalization_factor # Multiply by normalization_factor using broadcasting


def save_to_file(frames, path):
    """
    Saves the frame in the specified path as rows of ascii characters

    @param frame: a single matrix of 0s and 1s
    @param path: name of output file

    returns: nothing
    """
    gscale = " .:+*?%S#@"
    with open(path, "w") as file:
        for frame in frames:
            for i in range(len(frame)):
                rendered = ""
                for j in range(len(frame[0])):
                    rendered += gscale[int(frame[i][j])]
                rendered += "\n"
                file.write(rendered)
            file.write("\n")


def display_video(path, fps):
    """
    Displays the frames line by line read from path at the given fps

    @param path: name of text file
    @param fps: the frames per second to run the video

    returns: nothing
    """
    with open(path, "r") as f:
        frames = f.read().split("\n\n")
        for frame in frames:
            print(frame)
            time.sleep(1/fps)
            clear_terminal()


def clear_terminal():
    _ = os.system('clear')


def play_video(video_path, frame_data_path):
    print("Starting Extraction...")
    start = time.time()
    make_frames(video_path, frame_data_path)
    end = time.time()
    print(f"Extraction done, took {end - start} seconds")


    print("Playing Video...")
    time.sleep(5)
    video = cv.VideoCapture(video_path)
    fps = video.get(cv.CAP_PROP_FPS)
    video.release()
    display_video(frame_data_path, fps) 


if __name__ == "__main__":
    video_path = sys.argv[1]
    frame_data_path = video_path[:-4] + "_frames.txt"
    play_video(video_path, frame_data_path)
