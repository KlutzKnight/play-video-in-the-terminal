from PIL import Image
import cv2 as cv
import numpy as np
import time
import os
import sys
import shutil

def make_frames(in_path, out_path, ymax):
    """
    Makes the ascii art of each frame in video and saves it to out_path, normalizing it to [0, ymax]

    @param in_path: the video to extract the frames
    @param out_path: the output path to store the ascii art
    @param ymax: a positive integer

    returns: nothing
    """
    video = cv.VideoCapture(in_path)
    video_frames = []

    while video.isOpened():
        success, frame = video.read()

        # if frame is read correctly success is True
        if not success:
            print("Can't receive frame (stream end?). Saving...")
            break
        
        # Change to grayscale and resize
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        size = shutil.get_terminal_size()
        frame = Image.fromarray(frame).resize((size.columns, size.lines - 1))
        # Make image an ndarray and normalize it to [0, ymax]
        frame = np.asarray(frame)
        frame = normalize(frame, ymax)

        video_frames.append(frame)
    
    save_to_file(video_frames, out_path, ymax)
    video.release()


def normalize(matrix, ymax):
    """
    Normalized the matrix values from [0,255] to [0, ymax] using min-max scaling

    @param matrix: Matrix of values ranging from [0, 255]
    @param ymax: a positive integer

    returns: normalized matrix
    """
    normalization_factor = (ymax - 1)/255
    return matrix * normalization_factor # Multiply by normalization_factor using broadcasting


def save_to_file(frames, path, ymax):
    """
    Saves the frame in the specified path as rows of ascii characters, normalized to [0, ymax]

    @param frame: a single matrix of 0s and 1s
    @param path: name of output file
    @param ymax: a positive integer

    returns: nothing
    """
    gscale = {
        2: "@ ",
        10: "@#S%?*+:. ",
    }
    with open(path, "w") as file:
        for frame in frames:
            for i in range(len(frame)):
                rendered = ""
                for j in range(len(frame[0])):
                    rendered += gscale[ymax][int(frame[i][j])]
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
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux (POSIX systems)
    else:
        _ = os.system('clear')


def play_video(video_path, frame_data_path, ymax):
    print("Starting Extraction...")
    start = time.time()
    make_frames(video_path, frame_data_path, ymax)
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
    num_gray_values = int(sys.argv[2])
    play_video(video_path, frame_data_path, num_gray_values)