# segment_videos.py
# Ilse Daly (ilse.daly@bristol.ac.uk / ilsemdaly@gmail.com)
# 27 Oct 2017

# A code to segment a long video with many sections indicated by a 'beep' noise
# NOTE: you will need the vidseg module (packaged with this file)
# NOTE: tested on a linux machine with MTS videos

import numpy as np
import cv2
import os
import sys
from time import sleep
import matplotlib.pyplot as plt
import vidseg 

### **** INPUT PARAMETERS **** ###
folderName='/home/id12253/Documents/Labbook/Stomatopod/PodScan/Data/yellow_red/pod0/left' # name of folder with video
videoName='pod0.MTS' # name of video
audioName='vidwav.wav' # chosen name for audio
trialVidBaseName='t' # chosen base name for trials
trialVidFormat='MTS' # format of trial videos
trialVidFolder='tempVids' # chosen name for folder containing trial videos

threshVal=32100 # minimum threshold for aplitude of audio signal i.e. >threshold=beep
videoDuration=20 # chosen length of trial video
leadTime=5 # length of time in video before the beep

ffmpegPath='ffmpeg' # path to ffmpeg (i.e. 'ffmpeg' in my linux setup)
sampleRate=48000 # sample rate of audio file (48000 in my setup)

videoPath='%s/%s' % (folderName, videoName)
audioPath='%s/%s' % (folderName, audioName)
trialVidFolder='%s/%s' % (folderName, trialVidFolder)
vidseg.create_folder(trialVidFolder)

checkVideoPath=vidseg.check_file_exits(videoPath)
if checkVideoPath==False:
	message='Video file (%s) does not exist. Quitting program' % videoPath
	print message
	sys.exit(0)

checkAudioPath=vidseg.check_file_exits(audioPath)

if checkAudioPath==False:
	vidseg.make_wav(ffmpegPath,videoPath, audioPath)

reCheckAudioPath=False
while reCheckAudioPath==False:
	reCheckAudioPath=vidseg.check_file_exits(audioPath)
print 'Audio file created'

beepCheck=False
while beepCheck==False:
	time,signal,selTime,selSignal,beepTime=vidseg.digitise_wav(audioPath,sampleRate,threshVal)

	plt.figure(1)
	plt.plot(time, signal)
	plt.plot(beepTime,threshVal*np.ones(len(beepTime)),'ro')
	plt.ylabel('some numbers')
	plt.show()

	
	beepConfirm=raw_input('Have the beeps been correctly identified? [y/n]')
	if beepConfirm=='y':
		beepCheck=True
		
	elif beepConfirm=='n':
		message='Current amplitude threshold is %d, please enter new threshold value...  ' % threshVal
		threshVal=int(raw_input(message))

beepTime=np.sort(beepTime)

duration=vidseg.seconds_to_hms(videoDuration)
i=0
while i<len(beepTime):
	startTime=vidseg.seconds_to_hms(beepTime[i]-leadTime)
	trialVidPath='%s/%s_%d.%s'% (trialVidFolder,trialVidBaseName,i+1,trialVidFormat)

	vidseg.segment_video(ffmpegPath,videoPath,trialVidPath,startTime,duration)
	
	i=i+1
