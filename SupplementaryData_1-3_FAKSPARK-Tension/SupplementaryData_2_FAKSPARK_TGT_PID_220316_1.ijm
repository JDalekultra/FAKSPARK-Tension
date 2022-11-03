//***ParticlesOverTimeParticleAnalysisAlgorithm which produces a list of guessed fakspark droplets generated over time as measured by a TIRF microscopy timelapse of and x,y, intensity micrographs in a time series of a cell transfected with the FAKSPARK plasmid. 
//run("Record...");//Run to initiate the recording the session in the macro recorder 

//---First threshold the image and create a binary mask, using the TIRF timelapse
//run("Subtract Background...", "rolling=15 stack"); //This subtracts the background using the rolling ball background subtraction Rolling Ball Background function
//Press ctrl+alt+t and manually threshold the image so that only the FAKSPARK droplets are highlighted by the threshold, apply to whole stack, ensure the 'calculate threshold for each image' option in the dialogue box is unchecked to threshold the entire stack.
//run("Convert to Mask"); //The 'Convert to Mask' function is applied to the thresholded image with all options in the dialogue box unchecked. This will convert the image timelapse in a 8-bit image timelapse with a 0 intensity value of background pixels and 255 intensity value for FAKSPARK droplet pixels. 

//---ThenAnalyze the particles for the image and produce a list of particles in each frame

//run("Analyze Particles...", "size=0.10-20.00 display clear summarize add in_situ slice"); //Don not run this function unless to test a test frame .
//! Run the 'sliceAnPart' function with the directory to save the ROIs identified for each frame as the first arguement and the image name as the second arguement.
//printImageNames();//Run to print a list of image names for convinience and copy, past

name ="Inset_Composite-1-1-4.tif" //Type the name of the image timelapse with the extension in parenthesis 
saveDirectory = "D:\\WorkData\\SaveDirectory_220316\\WithWaterShed\\"; //Enter the directory with Read/Write privaleges in parenthesis, differences in syntax exist between Windows, Mac, and Linux

sliceAnPart(saveDirectory, name); //This will produce a list of particles and their statistics for each slice, this list of statistics is then saved as a .csv file which includes the number of identified particles for each frame. 
//---The log window will now contain a list of ROIs by frame which may be saves as a .csv file and graphed.
//---The function will also save each list of ROIs as individual ROI files for eawch frame of the image timelapse in a specified folder for further analysis and visualization.

function sliceAnPart(aveDirectory, name){//This will produce a list of particles and their statistics for each slice, this list of statistics is then saved as a .csv file which includes the number of identified particles for each frame. 
	selectImage(name);
	getDimensions(w, h, channels, slices, frames);		
	for(i=0;i<slices;i++){
		selectImage(name);
		Stack.setPosition(1, i, 1); //channel, slice, frame);
		run("Duplicate...", "title=dupImage");

		selectImage("dupImage");
		run("Convert to Mask");	
		//run("Watershed");//---comment in the watershed algorithm to increase the number of particles detected
		run("Analyze Particles...", "size=0.010-20.00 display clear summarize add in_situ slice");
		
		n = roiManager("count"); //Number of ROIs in the roiManager
		print(i+1, n);
		roiManager("Save", saveDirectory+"/ROIs_"+i+".zip");
		selectWindow("ROI Manager");
		run("Select All");
		roiManager("Delete");	
			
		selectWindow("ROI Manager");
		run("Close");
		
		selectImage("dupImage");
		wait(500);
		run("Close");
		for (k=1; k<=nImages; k++) { //this loop ensures the duplicate image, dupImage is closed
	   		selectImage(k);          
			tempName = getTitle; 
				if(tempName == "dupImage"){
					run("Close");
				}
			}
		wait(500);
		
	}
}


function printImageNames(){
	for (i=1; i<=nImages; i++) { //A647: 268, 492 __ 408, 798
	   	selectImage(i);          //488, 730 for TxRed W1, for W3 BG ~=600 cont. 490, 1000
		print(getTitle); //print the title of the selected image to the console
	} 
	selectWindow("Log");
}