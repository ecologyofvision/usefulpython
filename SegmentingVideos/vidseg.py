# MODULE vidseg
# Ilse Daly (ilse.daly@bristol.ac.uk / ilsemdaly@gmail.com)
# 27 Oct 2017

import numpy as np
import cv2
import os
import subprocess as sp
import sys
from time import sleep
import shutil
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from sklearn.cluster import MeanShift, estimate_bandwidth


# checks if a file exists, returns True or False
def check_file_exits(fileName):
	if os.path.isfile(fileName)==True:
		check=True
	else:
		check=False

	return check

# Checks if a foler exists. If it doesn't, it creates it. 
# If it does, it asks user if they want to overwrite the folder. If not, code
# is aborted
def create_folder(folderName):
	if os.path.isdir(folderName)==True:
		message='Folder (%s) already exists. Overwrite? [y/n] ' % folderName
		
		folderConfirm=raw_input(message)
		if folderConfirm=='y':
			print "Deleting folder"
			shutil.rmtree(folderName)
			print "Making folder"
			os.mkdir(folderName)
		elif folderConfirm=='n':
			print "Quitting"
			sys.exit(0)		
	else:
		print "Making folder"
		os.mkdir(folderName)

# converts seconds to a hh:mm:ss string format (assumes hh=00)
def seconds_to_hms(time):
	mins=int(time/60)
	secs=round(time-(mins*60))

	if secs==60:
		secs=0
		mins=mins+1

	if secs<10:
		s='0%d' % secs
	else:
		s='%d' % secs

	if mins<10:
		m='0%d' % mins
	else:
		m='%d' % mins

	start='00:%s:%s' % (m,s)

	return start

# uses ffmpeg to convert a video file to a wav file
def make_wav(ffmpegPath,videoPath, audioPath):
	sp.call([ffmpegPath,'-i',videoPath,'-acodec', 'pcm_s16le', '-ac', '2', audioPath])
	

# finds clusters of numbers in a 1D array
def find_clusters(x):
	X = np.array(zip(x,np.zeros(len(x))), dtype=np.float)
	bandwidth = estimate_bandwidth(X, quantile=0.1)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms.fit(X)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_
	labels_unique = np.unique(labels)
	n_clusters = len(labels_unique)

	groups=np.zeros(n_clusters)
	for k in range(n_clusters):
  		my_members = labels == k
   		z=X[my_members, 0]
    		groups[k]=np.mean(z)

	return groups

# finds the amplitude of the wav file with time, finds the time that the audio is above the 
# threshold amplitude, identifies the clusters of time, finds the mean and returns the average
def digitise_wav(audioName,sampleRate,threshVal):
	audio=read(audioName)
	digAudio=np.array(audio[1])
	signal=digAudio[:,0]	
	time=np.arange(float(len(signal)))/sampleRate
	index=signal>threshVal
	selTime=time[index]
	selSignal=signal[index]
	beepTime=find_clusters(selTime)

	return time, signal,selTime, selSignal,beepTime

# uses ffmpeg to segment a long video into individual trial videos with specific start times and durations
def segment_video(ffmpegPath,videoPath,trialVidPath,startTime,duration):
	sp.call([ffmpegPath,'-i',videoPath,'-vcodec', 'copy','-acodec','copy','-ss',startTime,'-t',duration, trialVidPath])
	




