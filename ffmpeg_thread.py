#####################
# ffmpeg_thread.py
#
#####################

# imports
import threading
import sys
import ffmpeg
import json
import os
import numpy as np
import time

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot

sys.path.insert(0,'..')
from params.param_loader import ParameterLoader

class FfmpegThread:
    
    # static member variables
    ffmpegThreadCount = 0
    def __init__(self):
        FfmpegThread.ffmpegThreadCount += 1
        print(f"Ffmepg instances: {FfmpegThread.ffmpegThreadCount}\n")

    def initialiseFfmpeg(self):
        pass
    
    def loadConfig(self):
        self.device_id  = None
        self.resolution = None
        (self.frame_width, self.frame_height) = self.resolution
        self.fps        = None
        self.use_enhance_image = None
        self.image_enhancer = None
    
    def showConfigs(self):
        print(f'Device ID    : {self.device_id}')
        print(f'Resolution   : {self.resolution}')
        print(f'FPS          : {self.fps}')
        print(f'Img Enhance  : {self.use_enhance_image}')
        print(f'Enhancer Type: DCE Zero')
    
    def runFfmpeg(self):
        pass

class UsbCameraThread(FfmpegThread):
    
    def __init__(self):
        FfmpegThread.__init__(self)
        self.loadConfig() # load config file
        self.initiateConnection()

    def loadConfig(self):
        config = ParameterLoader.loadJson("../params/configs/SocialDistanceVA_config.json")
        self.device_id  = config["device_id"]
        self.resolution = config["resolution"]
        (self.frame_width, self.frame_height) = self.resolution
        self.fps        = config["fps"]
        self.use_enhance_image = config["enhance_image"]
            
    def initiateConnection(self):
        self.bConnectionSuccess = False
        self.droppedFrames = 0
        
        # start ffmpeg thread for the particular webcam
        try:
            self.ffmpeg_thread = threading.Thread(target=self.runFfmpeg, args=())
            print("Starting ffmpeg thread")
            # self.ffmpeg_thread.daemon = True
            print("Set daemon to true")
            self.ffmpeg_thread.start()
            print(f'thread status: {self.ffmpeg_thread.is_alive()}')
            print("FFmpeg thread started")
            self.bConnectionSuccess = True
            print(f"Started ffmpeg thread with device: {self.device_id}")
            
        except:
            print(f"Could not start ffmpeg thread with device: {self.device_id}")
            self.bConnectionSuccess = False
            
    def runFfmpeg(self):
        print("run ffmpeg thread")

        self.ffmpegProcess = (ffmpeg
        .input(self.device_id)
        .filter('fps', fps=self.fps, round='up')
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(self.frame_width, self.frame_height))
        .run_async(quiet=True, pipe_stdout=True))

        print("ffmpeg process okay")

        self.frameGrabber = threading.Thread(target=self.grabNewFrame, args=())
        # self.frameGrabber.daemon = True
        self.frameGrabber.start()
        
    def grabNewFrame(self):
        while True:
            time.sleep(0.025) # sleep for a bit before trying to get the next frame
            
            # read frames from ffmpeg
            frame_size = self.frame_width * self.frame_height * 3 # 3 channels * resolution = total bytes of frame
            
            try:
                frame_size_in_bytes = self.ffmpegProcess.stdout.read(frame_size) # read the frame
            
            except:
                print("Error processing ffmpeg frame")
                return None
            
            if len(frame_size_in_bytes) == 0: # if frame is empty
                frame = None
            
            else:
                assert len(frame_size_in_bytes) == frame_size, 'No frame grabbed'
                frame = (np.frombuffer(frame_size_in_bytes, np.uint8).reshape([self.frame_height, self.frame_width, 3]))
                # print(type(frame))
                # print(frame.data)

                
class FfmpegWorker(FfmpegThread, QtCore.QObject):
    
    # signals
    tx_frame = pyqtSignal(np.ndarray)

    def __init__(self):
        FfmpegThread.__init__(self)
        QtCore.QObject.__init__(self)
        self.loadConfig() # load config file
        self.initiateConnection()

    def loadConfig(self):
        config = ParameterLoader.loadJson("../params/configs/SocialDistanceVA_config.json")
        self.device_id  = config["device_id"]
        self.resolution = config["resolution"]
        (self.frame_width, self.frame_height) = self.resolution
        self.fps        = config["fps"]
        self.use_enhance_image = config["enhance_image"]
            
    def initiateConnection(self):
        self.bConnectionSuccess = False
        self.droppedFrames = 0
        
        # start ffmpeg thread for the particular webcam
        try:
            self.ffmpeg_thread = threading.Thread(target=self.runFfmpeg, args=())
            print("Starting ffmpeg thread")
            # self.ffmpeg_thread.daemon = True
            print("Set daemon to true")
            self.ffmpeg_thread.start()
            print(f'thread status: {self.ffmpeg_thread.is_alive()}')
            print("FFmpeg thread started")
            self.bConnectionSuccess = True
            print(f"Started ffmpeg thread with device: {self.device_id}")
            
        except:
            print(f"Could not start ffmpeg thread with device: {self.device_id}")
            self.bConnectionSuccess = False
            
    def runFfmpeg(self):
        print("run ffmpeg thread")

        self.ffmpegProcess = (ffmpeg
        .input(self.device_id)
        .filter('fps', fps=self.fps, round='up')
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(self.frame_width, self.frame_height))
        .run_async(quiet=False, pipe_stdout=True))

        print("ffmpeg process okay")

        self.frameGrabber = threading.Thread(target=self.grabNewFrame, args=())
        # self.frameGrabber.daemon = True
        self.frameGrabber.start()
        
    def grabNewFrame(self):
        while True:
            time.sleep(0.025) # sleep for a bit before trying to get the next frame
            
            # read frames from ffmpeg
            frame_size = self.frame_width * self.frame_height * 3 # 3 channels * resolution = total bytes of frame
            
            try:
                frame_size_in_bytes = self.ffmpegProcess.stdout.read(frame_size) # read the frame
            
            except:
                print("Error processing ffmpeg frame")
                return None
            
            if len(frame_size_in_bytes) == 0: # if frame is empty
                frame = None
            
            else:
                assert len(frame_size_in_bytes) == frame_size, 'No frame grabbed'
                frame = (np.frombuffer(frame_size_in_bytes, np.uint8).reshape([self.frame_height, self.frame_width, 3]))
                # print(type(frame))
                self.tx_frame.emit(frame)

if __name__ == '__main__':
    u = UsbCameraThread()
    # u.showConfigs()
    # u.initiateConnection()
    
    
