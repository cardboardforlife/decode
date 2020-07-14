import numpy as np
import matplotlib.pyplot as plt
from lib_morse import *

if __name__ == '__main__':

    filename = 'vid.mp4'
    filename_folder = 'frames/frame'
    number_frames = convert_video_to_frames(filename,filename_folder)
    average_colour_frames = convert_frames_to_average_colour(filename_folder,number_frames,filter_rgb=(1,0,0))

    binary_average_frames = video_average_colour_to_binary(average_colour_frames,threshold=22)

    plt.figure()
    plt.plot(binary_average_frames*(max(average_colour_frames)-min(average_colour_frames))+min(average_colour_frames))
    plt.plot(average_colour_frames)
    plt.show()

    msg_decoded = decode_binary_to_ascii(binary_average_frames)
    print("message decoded: ",msg_decoded)