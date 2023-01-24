/*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*/

//Press ctrl+alt+t and manually threshold the image so that only the FAKSPARK droplets are highlighted by the threshold, apply to whole stack, ensure the 'calculate threshold for each image' option in the dialogue box is unchecked to threshold the entire stack.
//run("Convert to Mask"); //The 'Convert to Mask' function is applied to the thresholded image with all options in the dialogue box unchecked. This will convert the image timelapse in a 8-bit image timelapse with a 0 intensity value of background pixels and 255 intensity value for FAKSPARK droplet pixels. 

//---Then Analyze the particles for the image and produce a list of particles in each frame

//!For the spark calculation, no background subtraction was used
//makeRectangle(0, 0, 250, 250);
//run("Watershed");//---comment in the watershed algorithm to increase the number of particles detected
//run("Analyze Particles...", "size=0.010-500.00 display clear summarize add in_situ slice"); //Dont run this function unless to test a test frame 
sumROIInt();

//! Run the 'sliceAnPart' function with the image name as the only arguement.
//printImageNames();//Run to print a list of image names for convinience and copy, past

name = "C_371-4_5-1-T488-1.tif" //Type the name of the image timelapse with the extension in parenthesis 
saveDirectory = "D:\\WorkData\\FAKSPARK_s201030\\FAKSPARK_TGT_SparkCalculation\\Particles_1\\"; //Enter the directory with Read/Write privaleges in parenthesis, differences in syntax exist between Windows, Mac, and Linux

maxSize = 500.00;
numWaterShed = 2;

//run("Subtract Background...", "rolling=15 stack"); //This subtracts the background using the rolling ball background subtraction Rolling Ball Background function
//sliceAnPart(saveDirectory, name, maxSize, numWaterShed); //This will produce a list of particles and their statistics for each slice, this list of statistics is then saved as a .csv file which includes the number of identified particles for each frame. 
//---The log window will now contain a list of ROIs by frame which may be saves as a .csv file and graphed.
//---The function will also save each list of ROIs as individual ROI files for eawch frame of the image timelapse in a specified folder for further analysis and visualization.

//run("Analyze Particles...", "size=0.010-"+maxSize+" display clear summarize add in_situ slice");
//sumROIInt();

function sumROIInt(){//This will produce a list of particles and their statistics for each slice, this list of statistics is then saved as a .csv file which includes the number of identified particles for each frame. 
	print("\\Clear");

	n = roiManager("count"); //Number of ROIs in the roiManager
	intFI = 0;
	for(i=0;i<n;i++){
		roiManager("Select", i);
		ROIFI = getValue("IntDen")/1000;
		intFI = intFI+ROIFI;
	}
	print(intFI);
	
}


function sliceAnPart(saveDirectory, name, maxSize, numWaterShed){//This will produce a list of particles and their statistics for each slice, this list of statistics is then saved as a .csv file which includes the number of identified particles for each frame. 
	print("\\Clear");
	selectImage(name);
	getDimensions(w, h, channels, slices, frames);			
	for(i=0;i<101;i++){
		selectImage(name);
		Stack.setPosition(1, i, 1); //channel, slice, frame);
		run("Duplicate...", "title=dupImage");

		selectImage("dupImage");
		run("Convert to Mask");	
		for(k=0;k<numWaterShed;k++){	
			run("Watershed");//---comment in the watershed algorithm to increase the number of particles detected
		}
		run("Analyze Particles...", "size=0.010-"+maxSize+" display clear summarize add in_situ slice");
						
		n = roiManager("count"); //Number of ROIs in the roiManager
		print(i+1+", "+n);
		if(n>0){
			//roiManager("Save", saveDirectory+"/ROIs_"+i+".zip");
			a=1;
		}
		selectWindow("ROI Manager");
		if(n>0){
			run("Select All");
			roiManager("Delete");	
		}
			
		selectWindow("ROI Manager");
		run("Close");
		
		selectImage("dupImage");
		wait(100);
		run("Close");
		for (k=1; k<=nImages; k++) { //this loop ensures the duplicate image, dupImage is closed
	   		selectImage(k);          
			tempName = getTitle; 
				if(tempName == "dupImage"){
					run("Close");
				}
			}
		wait(100);
		
	}
}


function printImageNames(){
	for (i=1; i<=nImages; i++) { //A647: 268, 492 __ 408, 798
	   	selectImage(i);          //488, 730 for TxRed W1, for W3 BG ~=600 cont. 490, 1000
		print(getTitle); //print the title of the selected image to the console
	} 
	selectWindow("Log");
}