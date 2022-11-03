# -*- coding: utf-8 -*-
'''
This program produces kymograph figures, maximum intensity along the 
frame(time) axis plots and traces of two or three fluorescence intensity 
kymographs, and computes the frame difference between the first occurance 
of 75% of the maximum intensity in the tension fluorescence channel and 
first occurance of 75% of the maximum fluorescence intensity in the FAKSPARK 
fluorescence channel. Scroll to the bottom to designate the file paths for the 
fluorescence intensity kymographs, the order in which they appear in 
the folder, and the destination file path to store the data.
'''

#
from __future__ import division
from matplotlib import *
from matplotlib.pyplot import *
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt # since this was "from matplotlib.pyploy import *" above, you don't have to state things like plt.plot etc., you can just type plot, but actually you pretty much have to type plt.plot because other imported modules may have plot functions
import numpy as np # you have! to do this anc call the respective functions as np.sin(whatever) and sp.sin whatever in statements which are numberic or symbolic respectively 
import sympy as sp
import scipy as scp
import seaborn as sns
import pandas as pd
import matplotlib.animation as animation
from scipy import stats
import datetime
import random
import csv
import os
import math
import subprocess
import sys
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits import mplot3d

from PIL import Image
import skimage as sk
from skimage import segmentation

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']) #This prints to the console any packages called but not found/installed
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]  # But leave them of because of f pip issue 

#------------------------------------------------------------------------------

def list_dirs(dir):
	r = [] # this creates an emtpy array of any type
	for root, dirs, files in os.walk(dir):
		for name in dirs: #  dir to list the dirs, name is a newly created variable that somehow assigns the filename is the files category of the oswalk generated tuple
			r.append(os.path.join(root, name))

	return r

def list_files(dir):
	r = []
	rdirs = []
	for root, dirs, files in os.walk(dir):
		for i in files:
			r.append(i) # the file name as a string
			rdirs.append(root) # the path to the file as a string
			
	return r, rdirs      

def saiveKymo(filename, filepath):
	a=1
	filetype = ".svg"   
	newfiledir = os.path.join(filepath, "Kymograph")
	#must make and then check the folder name
	if(False == os.path.exists(newfiledir)):
		os.mkdir(newfiledir)
	print("\n\n\n",newfiledir,"\n\n\n")
	os.chdir(newfiledir)
	print("Output sent to "+os.getcwd())
	thyme = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
	plt.savefig(filename+thyme+filetype) #plots need to be saved directly after plt.plot() statement to save them all 
	#---Save Outputs to Text file
	'''
	txtFile = open(filename+thyme+".txt", "w") 
	txtFile.write(outPutString) 
	txtFile.close() 
	'''

def saiveGraph(filename, filepath):
	a=1
	filetype = ".svg"   
	newfiledir = os.path.join(filepath, "Graph")
	#must make and then check the folder name
	if(False == os.path.exists(newfiledir)):
		os.mkdir(newfiledir)
	print("\n\n\n",newfiledir,"\n\n\n")
	os.chdir(newfiledir)
	print("Output sent to "+os.getcwd())
	thyme = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
	plt.savefig(filename+thyme+filetype) #plots need to be saved directly after plt.plot() statement to save them all 
	#---Save Outputs to Text file

def saveTrace(filepath, traceName, trace):
	newfiledir = os.path.join(filepath, "Trace_Values")
	#must make and then check the folder name
	if(False == os.path.exists(newfiledir)):
		os.mkdir(newfiledir)
	os.chdir(newfiledir)
	#---Comment the below to not save
	np.savetxt(traceName, trace, delimiter=',')
	
def getDat(dirName, tensChannel, FAKChannel, mainStr, saivePath):

	#---Go through each item in the folder and all subfolders
	flList = os.listdir(dirName)# must have the 'r' before the file name...cuz
	dlist = list_dirs(dirName) #dlist is the list of directories, they are strings02
	rlist, rdlist = list_files(dirName) # rlist is the list of files as strings, rdlist is the list off full pathnames of the files

	#---Execute selection condition commands
	phrasze = '' # '' is a character in all files, it is not a character in no files.
	fileAr = [] #array of full file paths to process
	filenmAr = [] #Array of file names

	#---Select all files to be processed
	for i in range(0,len(rdlist)):	# for all files in the directory
		pathnm = os.path.join(rdlist[i], rlist[i]) #set the concatenated folder and file name as the pathname, pathnnm. 	
		if(pathnm.endswith('.tif') and phrasze in str(pathnm)):
			fileAr.append(os.path.join(rdlist[i], rlist[i])) # make the array file locations to be graphed
			filenmAr.append(rlist[i])
	
	#---Initialize the figure for plotting intensity over time of the kymograph
	fig = plt.figure() # The variable which contains the figure to print
	ax1 = plt.subplot(1,1,1) #The variable which contains the axis object which data will be plotted on
	#---Initialize arrays to store max intensity and time(frames) in
	Peaks = []#the array to put the X and Y coordinates for the Peak tension and FAK times
	Ys = []

	#---Create or recognize the folder 
	roiName = str(os.path.basename(dirName))
	roiFilePathName = os.path.join(saivePath, roiName)
	if(False == os.path.exists(roiFilePathName)):
		os.mkdir(roiFilePathName)

	for i in range(0,len(fileAr)):#---Iterate through all the files in the folder
		X, Y, im1, XAr, imj = IP1(fileAr[i], filenmAr[i], fig, ax1, i) #---IP1 returns the plot and image(imj) from the kymograph image file and 
		#np.savetxt(dirName+'\C'+str(i+1)+'_Trace.csv', im1, delimiter=',')#---SAVE the trace of the curve quantification in the roi folder
		#cellName = str(filenmAr[i][:-4])

		#---The below is to save the trace in saivePath, comment the np.savetxt option in the saiveTrace function to save the trace. 
		timeStamp = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
		roiName = str(os.path.basename(dirName))

		saveTrace(roiFilePathName,'c'+roiName+'_C'+str(i+1)+'_'+timeStamp[10:]+'Trace.csv', im1)#---SAVE the trace of the curve quantification in the roi folder
		Peaks.append(X) #note this also loads axes to the plot

		Ys.append(Y)

	Peaks = np.array(Peaks)
	Ys = np.array(Ys)
	DelayTime = abs(Peaks[tensChannel]-Peaks[FAKChannel])#---Calculate the Delay time between tension and FAK in frames, Ensure the appropriate channels are set in the tensChannel and FAKChannel variables

	#---Convert Arrays to Strings
	PEAKS = np.array_str(Peaks)
	YS = np.array_str(Ys)	
	DelayTime = str(DelayTime)
	
	mainStr += '\n'+dirName
	mainStr += '\nFrames at which intensity exceed threshold of 75% max intensity'+PEAKS+YS
	mainStr += "\nDelay Time : "+DelayTime+" Frames\n" 
		
	plt.text(0, 0.97, str(DelayTime)+" Frames")
	Xs = Peaks #Get the right time to graph
	ax1.scatter(Xs,Ys, s=50, facecolors='none', edgecolors='k')#Plot the 0.75 value	

	left  = 0.3  # the distance between the left side of the subplots and the left side of the figure window, 0 is right on the figure edge
	right = 0.9    # the right side of the subplots of the figure, 1.0 is right on the figure edge
	bottom = 0.2   # the bottom of the subplots of the figure
	top = 0.9      # the top of the subplots of the figure
	wspace = 0.4   # the amount of width reserved for space between subplots,
		       # expressed as a fraction of the average axis width
	hspace = 0.75	# the amount of height reserved for space between subplots,
               		# expressed as a fraction of the average axis height
	mpl.pyplot.subplots_adjust(left, bottom, right, top, wspace, hspace) #this affectively affects the indent!

	fig.set_size_inches(3.7,3)
	
	plt.show()
	
	#---Save the plot in the saivePath
	saiveGraph(roiName, roiFilePathName)

	#---Plot the individual kymographs 
	fig2 = plt.figure()	

	ax2 = fig2.add_subplot()
	ax2.set_ylabel("Frames")
	
	imagecmapAr0 = ['Reds', 'Greens', 'Blues']
	imagecmapAr1 = ['Greens', 'Reds', 'Blues']
	
	if(tensChannel==0):
		imagecmapAr = imagecmapAr0 
	if(tensChannel==1):
		imagecmapAr = imagecmapAr1 

	font = {'family': 'Arial', # this kind of notation is very useful
        'color':  'black', 
        'weight': 'bold',
        'size': 12,
        }	

	ax2.set_xlabel("Distance, ____", fontdict=font)
	ax2.set_ylabel("Time, Frames", fontdict=font)
	
	plt.axis('off')

	#---Graphing
	for i in range(0,len(fileAr)):#---Iterate over and display all the images in the folder
		imj = IP2(fileAr[i], filenmAr[i], fig2, ax1, i) #---IP2 returns the image
		#np.savetxt(dirName+'\C'+str(i+1)+'_Trace.csv', im1, delimiter=',')#---SAVE the trace of the curve quantification in the roi folder
		#cellName = str(filenmAr[i][:-4])
		timeStamp = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))#This creates a string of the current time for labeling and accounting
		roiName = str(os.path.basename(dirName))#This makes a string of the folder being processed which is the cell FAK/tension/paxillin ROI in the micrograph
		ax2 = fig2.add_subplot(1,3,i+1)
		ax2.imshow(imj, cmap=imagecmapAr[i])

		g = imj
		gg = ax2.imshow(g, cmap=imagecmapAr[i])
		#gg = set_array(g)
		cbar = plt.colorbar(gg, cmap=imagecmapAr[i])

		#ax2.get_xaxis().set_visible(False)

		#plt.axis('off')

	fig2.set_size_inches(6.1,2)

	#---Save the kymograph traces
	saiveKymo(roiName, roiFilePathName)#Save Kymo

	return mainStr

def IP1(pathName, title, fig, ax1, i):	
		
	imor = imread(pathName) #read the image from the path into the variable imor
	imj = sk.img_as_int(imor) #gives a x,y numpy array
	im1 = sk.img_as_int(imor) #gives a x,y numpy array
	im1 = im1.max(axis=1) #creates a 1d numpy array of the max values of the indicated axis of the array, axis=1 gives time on x axis and distance on y axi. This creates an array of the max intensity value on the x(distance) axis.
	mx = max(im1)
	mn = min(im1)

	im1 = (im1-mn)/(mx-mn) #Array normalized on a scale of 0-1
	np.append(im1,0.0) #makes the last datapoint zero, this is so graph looks nice using the 'fill under' option.
	
	#---get the point where the graph is more than 0.75 of its maximum
	maxInd = np.where(im1 > (np.amax(im1)*0.75)) #returns a tuple of the index where of max(np.amax) and the datatype in an array
	thresholdFrame = maxInd[0][0] #the first item in the array is the first time where the intensity of the im1(the simplified kymograph) is >75% of the maximum value. This is taken to be the threshold point of fluorescence accumulation due to tension/FAK/paxillin.
	XAr = np.arange(0,len(im1)) #Make an array filled with the indexes of im1.
	thresholdValue = im1[thresholdFrame]#This is the frame and intensity value of the threshold frame exceeding 75% max intensity in the kymograph.
	#---The plot is im1 vs Xar
	#ax1.imshow(im1, cmap="gray") 

	font = {'family': 'Arial', # this kind of notation is very useful
        'color':  'black', 
        'weight': 'bold',
        'size': 12,
        }	
	
	cmapAr0 = [plt.cm.OrRd, plt.cm.Greens, plt.cm.Greens]#OrRd Blues
	colourAr0 = ['r', 'g', 'b', 'b', 'r', 'g', 'b', 'b']	
	
	cmapAr1 = [plt.cm.Greens, plt.cm.OrRd, plt.cm.Greens]#OrRd Blues
	colourAr1 = ['g', 'r', 'b', 'b', 'r', 'g', 'b', 'b']	

	if(tensChannel==0):
		cmapAr = cmapAr0
		colourAr = colourAr0
	if(tensChannel==1):
		cmapAr = cmapAr1
		colourAr = colourAr1

	ax1.set_xlabel("Time, Frames", fontdict=font)
	ax1.set_ylabel("Norm. Max. Fluorescence, A.U.", fontdict=font)
	ax1.set_title(title, fontdict=font)	
	ax1.plot(XAr, im1, color=colourAr[i])
	ax1.fill_between(XAr, im1, 0, color=colourAr[i], alpha=0.2)

	return thresholdFrame, thresholdValue, im1, XAr, imj

def IP2(pathName, title, fig, ax1, i):	
		
	imor = imread(pathName)#read the image from the path
	imj = sk.img_as_int(imor) #gives a x,y numpy array
	return imj

'''---The kymographs must be two separate tiff files stored in a folder which is in the first index and the actual folder in the second:
Path = [[r'C:PATH\TOKYMOGRAPHFOLDER'], ['KYMOGRAPHFOLDER']]
As many kymograph folders can be designated as necessary.
'''

Path0 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\KymosFor210205_HeLaFAKSPARKIFPPax_STORM'], 
				["Cell_062_ROI2.3"]]

Path1 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\KymosFor210205_HeLaFAKSPARKIFPPax_STORM'], 
				["Cell_062_ROI2.3",
		    "Cell_062_ROI2.4",
			 "Cell_062_ROI2", 
			 "Cell_074_ROI8", 
			 "Cell_074_ROI1"]]

Path2 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\210603_HeLaFAKSpark\HairpinCy3B\Cell_3-6'],
		 ['ROI_2', 
	'ROI_3', 
	'ROI_4', 
	'ROI_5', 
	'ROI_7', 
	'ROI_8']]

Path3 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\210609_HeLaFAKIFP_Cy3BHairpin_STORM\Analysis\Kymos'],
		 ['ROI_1', 'ROI_2', 'ROI_3']]

Path4 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\210613_HairPinCy3B_HeLa_FAK_TIRF\Analysis\Kymos'],
		 ['ROI_1','ROI_2', 'ROI_3', 'ROI_4', 'ROI_5', 'ROI_6', 'ROI_7']]

Path5 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\210707_HeLaFAKIFP_Cy3BHairpin_STORM\Processing\Cell_014\ROIs'],
		 ['ROI_1']]

Path6 = [[r'D:\WorkData\FAKSPARK_s201030\19pNHP_FAKSPARK_MicroscopyData\Used\210707_HeLaFAKIFP_Cy3BHairpin_STORM\Processing\Cell_015\ROIs'],
		 ['ROI_1', 'ROI_2', 'ROI_3']]

'''
Each File in the second intex of Path# must contain two .tif files which are the kymographs of the FAK and tension channel set which order the kymographs appear in the variable below. The third .tif file is assumed to be the paxillin channel.
'''
tensChannel = 0 #0 if tension is first, 1 if second
FAKChannel = 1  #0 if FAKSPARK is first, 1 if second 

'''
The kymograph .tif files are then processed to a plot 
Save the graph
'''

#---!!!ensure saveTrace(...) is off if testing!!!!
mainStr = '' #String to pring all text at the end in the consol.
cellFilePath = Path6 #If multiple path variables are present, choose which to process.

saivePath = r'D:\WorkData\SaveDirectory_220316\SavePath\Path6'

for i in range(0, len(cellFilePath[1])): #ahh ineed the length of the second index!!!
	filepath = os.path.join(cellFilePath[0][0], cellFilePath[1][i])
	mainStr = getDat(filepath,tensChannel,FAKChannel, mainStr, saivePath)
#---Print the data 
print(mainStr)



plt.show()