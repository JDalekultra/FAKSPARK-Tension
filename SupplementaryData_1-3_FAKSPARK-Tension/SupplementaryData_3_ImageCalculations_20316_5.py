# -*- coding: utf-8 -*-
'''
This program subtracts the fluorescence bleedthrough and background of from 
fluorescence micrographs and saves the result in a separate file. Scroll to 
the end to designate flruoescence background image file(bit depth of target 
images), the path for the images to be processed(read code comments for 
dimensional information), and target directory to save processed images. 
'''


from __future__ import division
import numpy as np # you have! to do this anc call the respective functions as np.sin(whatever) and sp.sin whatever in statements which are numberic or symbolic respectively 
import os
import subprocess
import sys
import skimage as sk

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']) #This prints to the console any packages called but not found/installed
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]  # But leave them of because of f pip issue 

#------------------------------------------------------------------------------

def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

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
	
def getDat(dirName, tensChannel, FAKChannel, mainStr, saivePath, blankPath):
	
	#---Go through each item in the folder and all subfolders
	flList = os.listdir(dirName)# must have the 'r' before the file name...cuz
	dlist = list_dirs(dirName) #dlist is the list of directories, they are strings02
	rlist, rdlist = list_files(dirName) # rlist is the list of files as strings, rdlist is the list off full pathnames of the files
	
	#---Execute selection condition commands
	phrasze = '' # '' is a character in all files, it is not a character in no files.
	fileAr = []
	filenmAr = []
	
	#---Select all files to be processed
	for i in range(0,len(rdlist)):	# for all files in the directory
		pathnm = os.path.join(rdlist[i], rlist[i]) #set the concatenated folder and file name as the pathname, pathnnm. 	
		if(pathnm.endswith('.tif') and phrasze in str(pathnm)):
			fileAr.append(os.path.join(rdlist[i], rlist[i])) # make the array file locations to be graphed
			filenmAr.append(rlist[i])
	
	for k in range(0,len(fileAr)):#---Graph all the files in the folder
		X, Y, im1, XAr = IP1(fileAr[k], filenmAr[k], k, blankPath) #---IP1 makes the plot from the image file and 
	
	return mainStr

def IP1(pathName, title, i, blankPath):	
	
	title = title[:-4]
	
	#imj = sk.external.tifffile.imread(r'D:\WorkData\FAKSPARK_s201030\MicroscopyData\Used\210707_HeLaFAKIFP_Cy3BHairpin_STORM\Processing\Cell_014\Cell_014_Cropped.tif')
	imj = sk.external.tifffile.imread(pathName)
	#---returns an np.ndarray of [frame][channel][x][y]
		
	#---channels as indexes of the array 0:RICM, 1:TIRF488, 2:TIRF561, 3:Brightfield, 4:DAPI in the cell body focal plane, 5:FITC in the cell body focal plane. 
	imA = imj[1][:][:]#For our channel configuration, this is the TIRF
	imB = imj[2][:][:]
	im3 = imA-imB*0.6773 #Their is a constand bleedthrough ration of imB channel into imA
	im3 = im3.clip(min=0)

	BGT561 = sk.external.tifffile.imread(os.path.join(blankPath[0][0], blankPath[1][0]))
	
	T561 = imj[2][:][:]-BGT561
	T561 = T561.astype(np.int16)
	T561 = T561.clip(min=0)

	a = imj[0][:][:] #RICM
	b = im3 #Bleedthrough subtracted TIRF 488 phospho-FAKY397
	c = T561 #Background subtracted TIRF 561 TGT tension
	d = imj[3][:][:] #Brightfield
	e = imj[4][:][:] #DAPI in the cell body focal planeFIT
	f = imj[5][:][:] #FITC in the cell body focal plane.

	output = np.array([a,b,c,d,e,f])
	output = output.astype(np.uint16)
	
	print(output.shape)
	
	os.chdir(saivePath)
	sk.external.tifffile.imsave(title+".tif", output)
	
	return 0, 0, imj, 0

#------------------------------------------------------

tensChannel = 1
FAKChannel = 0


Path1 = [[r'D:\WorkData\FAKSPARK_s201030\HeLa_phosphoFAKY397_FAKSPARK_TGT_MicroscopyData1\211001_HeLaFAKphosY396_TGT_90minInc_STORM_processing\12pN1'], 
				["Tiffs"]] #The path to the background fluorescence image used to background subtract the TIRF 561 nm fluorescence channel.

blankPath = [[r'D:\WorkData\FAKSPARK_s201030\HeLa_phosphoFAKY397_FAKSPARK_TGT_MicroscopyData1\211001_HeLaFAKphosY396_TGT_90minInc_STORM_processing\12pN1\Blanks'], 
				["T561_Blankc_153-1.tif"]]#The path to the background fluorescence image used to background subtract the TIRF 561 nm fluorescence channel.

saivePath = r'D:\WorkData\SaveDirectory_220316\ProcessingConfirmation' #The path to the folder in which the processed images will be saved.

mainStr = '' #String to pring all text at the end

cellFilePath = Path1 #This is in case multiple Path variables are used

print("Used Directory ",len(cellFilePath[1])) 
for i in range(0, len(cellFilePath[1])): #Iterate over all the files in the path which contain the '.tif' prefix.
	filepath = os.path.join(cellFilePath[0][0], cellFilePath[1][i])
	print(filepath)
	mainStr = getDat(filepath,tensChannel,FAKChannel, mainStr, saivePath, blankPath)
#---Print the data concerning the file processing. 
print(mainStr)

#plt.show()