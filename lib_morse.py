import numpy as np
import blinkstick
import time
import cv2
from PIL import Image

dico_morse = {"A":"sl",
             "B":"lsss",
             "C":"lsls",
             "D":"lss",
             "E":"s",
             "F":"ssls",
             "G":"lls",
             "H":"ssss",
             "I":"ss",
             "J":"slll",
             "K":"lsl",
             "L":"slss",
             "M":"ll",
             "N":"ls",
             "O":"lll",
             "P":"slls",
             "Q":"llsl",
             "R":"sls",
             "S":"sss",
             "T":"l",
             "U":"ssl",
             "V":"sssl",
             "W":"sll",
             "X":"lssl",
             "Y":"lsll",
             "Z":"llss",
             " ":" ",
             "":"",
             "0":"lllll",
             "1":"sllll",
             "2":"sslll",
             "3":"sssll",
             "4":"ssssl",
             "5":"sssss",
             "6":"lssss",
             "7":"llsss",
             "8":"lllss",
             "9":"lllls",
             " ":" ",
             ",":"llssll",
             ".":"slslsl"
             }

dico_morse_decoding =  {v: k for k, v in dico_morse.items()}

def find_blinkstick():
    stick = blinkstick.find_first()
    stick.set_color(red = 0, green = 0, blue = 0)
    print("Blinkstick found!")
    return stick

def encode_morse_message(msg):
    msg = msg.upper()
    encode_morse = []
    for letter in msg:
        encode_morse.append(dico_morse[letter])
    return encode_morse

def blink_morse(msg_morse,stick,dot,colour=(1,0,0)):
    dico_time_morse = {"s" : dot,
                       "l" : 3*dot,
                       " ":0}
    print("Sending message...")
    time.sleep(.5)
    for m in msg_morse:
        for j,i in enumerate(m):
            stick.set_color(red = 255*colour[0], green = 255*colour[1], blue = 255*colour[2])
            time.sleep(dico_time_morse[i])
            stick.set_color(red = 0, green = 0, blue = 0)
            if j < len(m): time.sleep(dot) 
        if m == " ":
            time.sleep(7*dot)
        else:
            time.sleep(3*dot)
        stick.turn_off()
    print("Message sent.")
        
def send_message_morse(msg,stick,dot=.5):
    msg_in_morse = encode_morse_message(msg)
    print("Message encrypted!")
    blink_morse(msg_in_morse,stick,dot)
    
def filter_color_image(img,r_filter=1,g_filter=1,b_filter=1):
    height,width = img.size
    image_data=img.load()
    for loop1 in range(height):
        for loop2 in range(width):
            r,g,b = image_data[loop1,loop2]
            image_data[loop1,loop2] = r*r_filter,g*g_filter,b*b_filter
            
def convert_video_to_frames(filename,filename_folder):
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()
    assert success == True
    count_write = 0
    successes = 0
    while success:
        cv2.imwrite(filename_folder+"%d.jpg" % count_write, image)     # save frame as JPEG file      
        success,image = vidcap.read()
#         print('Read a new frame: ', success)
        count_write += 1
        successes += 1.*success
    successes = int(successes)+1
    if successes == count_write:
        print("Video successfully converted to {} frames.".format(count_write))
    else:
        print("Not all images converted to frames: {} out of {}".format(successes,count_write))
    return count_write

def convert_frames_to_average_colour(filename_folder,N_files,filter_rgb=(1,0,0)):
    average_frames = []
    for count_read in range(N_files):
#         print(count_read) if count_read%10==1 else None
        img = Image.open(filename_folder+"%d.jpg" % count_read)
        filter_color_image(img,*filter_rgb) if filter_rgb!=(1,1,1) else None
        colors_img = img.getdata()
        average_frames.append(np.mean(colors_img))
    average_frames = np.array(average_frames)
    return average_frames

def video_average_colour_to_binary(average_colours,threshold=22):
    return 1.*(average_colours>threshold)

def decode_binary_to_morse(average_frames,len_short=(2,4),len_long=7,len_next_char=(9,12),len_space=30):
    signal_morse = []
    letter_morse = []
    count1 = 0
    count0 = 0
    for b in binary_average_frames:
        if b == 1.:
            count1+=1.
        if b == 0.:
            count0+=1.

        if b == 0. and (count1 >= len_short[0] and count1 <=len_short[1]):
            letter_morse.append("s")
            count1 = 0.
            count0 = 0.
        if b == 0. and (count1 > len_long):
            letter_morse.append("l")
            count1 = 0.
            count0 = 0.

        if b == 1. and count0 > len_next_char[0] and count0<len_next_char[1]:
            signal_morse.append(''.join(letter_morse))
            letter_morse=[]
            count1 = 0.
            count0 = 0.
        if b == 1. and count0 >= len_space:
            signal_morse.append(''.join(letter_morse))
            signal_morse.append(" ")
            letter_morse=[]
            count0=0.
            count1=0.
    signal_morse.append(''.join(letter_morse))
    return signal_morse

def decode_morse(msg_morse):
    message_decoded = []
    for char in msg_morse:
        message_decoded.append(dico_morse_decoding[char])
    message_decoded = ''.join(message_decoded)
    return message_decoded

def decode_binary_to_ascii(average_frames):
    msg_morse = decode_binary_to_morse(average_frames)
    return decode_morse(msg_morse)