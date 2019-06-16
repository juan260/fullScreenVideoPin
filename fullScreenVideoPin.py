'''
fullScreenVideoPin.py

This code has been designed to be used in a Raspberry pi B3+. It is not 
intended to work anywhere else.

This module recieves as an argument a path to a video (only tested with
mp4 format)

When pin 23 of the Raspberry is connected to the ground of the board
the video will be displayed. The video is continiously playing on the 
background and doesn't stop when the pin is disconected. When that happens
it is no longer displayed, and a black frame is displayed instead.

To stop the program, just hit the 'q' key.

TODO:
    - The frame shown when the pin is disconnected is should be black
        but it is not.
    - The video frames are displayed at the wrong rate, maybe because
        of the limitations of the Raspberry board.

'''

import RPi.GPIO as GPIO
import time

import os
import sys
import Tkinter as tkinter
import numpy as np
import gobject
import gst

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#while(1):
#    time.sleep(1)
#    print(GPIO.input(23))

import cv2
import numpy as np

file_name = sys.argv[1]
window_name = "window"
interframe_wait_ms = 30

cap = cv2.VideoCapture(file_name)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 1)

while (True):
    ret, frame = cap.read()
    if not ret:
        print("Reached end of video.")
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
    if(GPIO.input(23)==0):
        frame=np.zeros(frame.shape, np.int8)
    cv2.imshow(window_name, frame)
    if cv2.waitKey(interframe_wait_ms) & 0x7F == ord('q'):
        print("Exit requested.")
        break

cap.release()
cv2.destroyAllWindows()

#def on_sync_message(bus, message, window_id):
#    if not message.structure is None:
#        if message.structure.get_name() == 'prepare-xwindow-id':
#            image_sink = message.src
#            image_sink.set_property('force-aspect-ratio', True)
#            image_sink.set_xwindow_id(window_id)

#gobject.threads_init()

#window = tkinter.Tk()
#window.geometry('500x400')
#video = tkinter.Frame(window, bg='#000000')
#video.pack(side=tkinter.BOTTOM,anchor=tkinter.S,expand=tkinter.YES,fill=tkinter.BOTH)
#window_id = video.winfo_id()
#player = gst.element_factory_make('playbin2', 'player')
#player.set_property('video-sink', None)
#player.set_property('uri', 'file://%s' % (os.path.abspath(sys.argv[1])))
#player.set_state(gst.STATE_PLAYING)

#bus = player.get_bus()
#bus.add_signal_watch()
#bus.enable_sync_message_emission()
#bus.connect('sync-message::element', on_sync_message, window_id)

#window.mainloop()
