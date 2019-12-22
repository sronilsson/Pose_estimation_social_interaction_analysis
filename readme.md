#### Python tool to analyse time spent in different open field areas based on pose estimation data from [deeplabcut](https://github.com/AlexEMG/DeepLabCut) 

![alt-text-1](/images/open_field.gif "open field")

##### Video example of data output on [YouTube](https://youtu.be/Q2ByLfwJIaw)

##### Tutorial

1. Place tracking files from DLC in **tracking_data** folder

2. Place video files in **videos**  folder

3. If visualizing the data, place the frames in the **input_frames** folder, within a subfolder with the same name as the video (without file ending). 

4. Run the py files in the order 1,2,3,4,5:
    
    * 1_Rename_files.py standardize all the tracking file names.
    * 2_correct_devs_mov.py corrects large tracking innacuracies by removing large 'jumps' in relation to the animal size.
    * 3_Specify_coordinates.py lets the user define the bounding boxes of the regions of interest (ROI) in each video using [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html).
    * 4_Analyze_data.py analyzes the time spent in each (ROI). The fps of the videos is defined on Line 16.
    * 5_visualize_data.py to plot overlays on frames using OpenCV.

 

   


 
 


  
