import os
import cv2
import pandas as pd
import numpy as np
from collections import deque
trackingFilesList = []

trackingFilesDir = r"Z:\DeepLabCut\OpenField_analysis\tracking_data"
coordinateFile = r"Z:\DeepLabCut\OpenField_analysis\py_files\coordinates.csv"
framesDirIn = r"Z:\DeepLabCut\OpenField_analysis\input_frames"
framesDirOut = r"Z:\DeepLabCut\OpenField_analysis\output_frames"
outPutDataPath = r"Z:\DeepLabCut\OpenField_analysis\outputData"
pd.options.mode.chained_assignment = None

if not os.path.exists(framesDirOut):
    os.makedirs(framesDirOut)
fps = 15
secondsToAnalyze = 150 * fps
oneFrameTime = round((1/fps), 2)
timeList = np.arange(oneFrameTime, secondsToAnalyze, oneFrameTime)
timeList = list(np.around(np.array(timeList), 2))
topCornerList = []
BottomLeftCornerList = []
cageTime_List = []
videoName_List = []
outputDf = pd.DataFrame()
coordsDf = pd.read_csv(coordinateFile)
coordsDf = coordsDf.rename(columns={"Unnamed: 0": "Video_name"})
csvFiles = []

for i in os.listdir(trackingFilesDir):
    if i.__contains__(".csv"):
        file = os.path.join(trackingFilesDir, i)
        trackingFilesList.append(file)

for currentTrackingFile in trackingFilesList:
    print(currentTrackingFile)
    listPaths_mouse1 = deque(maxlen=600)
    topLeftCorner_time = 0
    BottomLeftCorner_time = 0
    indDf = pd.DataFrame()
    indDf['Time'] = timeList
    indDf['Time_top_corner'] = 0
    indDf['Time_bottom_corner'] = 0
    indDf['Time_cage'] = 0
    Cage_time = 0
    topLeftFrameNoList = []
    bottomLeftFrameNoList = []
    cageFrameNoList = []
    loop = 0
    currentTrackingFileName = os.path.basename(currentTrackingFile)
    currentTrackingFramedFolder = currentTrackingFileName.replace('.csv', '')
    currentTrackingFileName = currentTrackingFileName.replace('.csv', '.mp4')
    curframesFolder = os.path.join(framesDirIn, currentTrackingFramedFolder)
    imageSaveDir = os.path.join(framesDirOut, currentTrackingFramedFolder)
    if not os.path.exists(imageSaveDir):
        os.makedirs(imageSaveDir)
    currentVidCoords = coordsDf.loc[coordsDf['Video_name'] == currentTrackingFileName]
    topLeftCorner_x1 = int(currentVidCoords['Top_left_corner_top_left_x'])
    topLeftCorner_x2 = int(currentVidCoords['Top_left_corner_bottom_right_x'])
    topLeftCorner_y1 = int(currentVidCoords['Top_left_corner_top_left_y'])
    topLeftCorner_y2 = int(currentVidCoords['Top_left_corner_bottom_right_y'])
    bottomLeftCorner_x1 = int(currentVidCoords['Bottom_left_corner_top_left_x'])
    bottomLeftCorner_x2 = int(currentVidCoords['Bottom_left_corner_bottom_right_x'])
    bottomLeftCorner_y1 = int(currentVidCoords['Bottom_left_corner_top_left_y'])
    bottomLeftCorner_y2 = int(currentVidCoords['Bottom_left_corner_bottom_right_y'])
    CageLeftCorner_x1 = int(currentVidCoords['Cage_top_left_x'])
    CageLeftCorner_x2 = int(currentVidCoords['Cage_left_corner_bottom_right_x'])
    CageLeftCorner_y1 = int(currentVidCoords['Cage_left_corner_top_left_y'])
    CageLeftCorner_y2 = int(currentVidCoords['Cage_left_corner_bottom_right_y'])
    columnHeaders = ["scorer","Nose_x", "Nose_y","Nose_p","Left_ear_x", "Left_ear_y", "Left_ear_p", "Right_ear_x", "Right_ear_y", "Right_ear_p", "Centroid_x", "Centroid_y", "Centroid_p", "Tail_base_x", "Tail_base_y", "Tail_base_p"]
    curTrackingDf = pd.read_csv(currentTrackingFile, names=columnHeaders)
    curTrackingDf = curTrackingDf.drop(curTrackingDf.index[[0]])
    curTrackingDf = curTrackingDf.reset_index()
    curTrackingDf = curTrackingDf.apply(pd.to_numeric)
    curTrackingDf = curTrackingDf.astype(int)
    for index, row in curTrackingDf.iterrows():
        if (((topLeftCorner_x1-10) <= int(row['Nose_x']) <= (topLeftCorner_x2+10)) and ((topLeftCorner_y1-10) <= row['Nose_y'] <= (topLeftCorner_y2+10)) or ((topLeftCorner_x1-10) <= int(row['Centroid_x']) <= (topLeftCorner_x2+10)) and ((topLeftCorner_y1-10) <= row['Centroid_y'] <= (topLeftCorner_y2+10))):
            topLeftCorner_time = round((topLeftCorner_time + (1/fps)), 2)
            topLeftFrameNoList.append(index)
        if (((bottomLeftCorner_x1-10) <= int(row['Nose_x']) <= (bottomLeftCorner_x2+10)) and ((bottomLeftCorner_y1-10) <= row['Nose_y'] <= (bottomLeftCorner_y2+10)) or ((bottomLeftCorner_x1-10) <= int(row['Centroid_x']) <= (bottomLeftCorner_x2+10)) and ((bottomLeftCorner_y1-10) <= row['Centroid_y'] <= (bottomLeftCorner_y2+10))):
            BottomLeftCorner_time = round((BottomLeftCorner_time + (1/fps)), 2)
            bottomLeftFrameNoList.append(index)
        if (((CageLeftCorner_x1-10) <= int(row['Nose_x']) <= (CageLeftCorner_x2+10)) and ((CageLeftCorner_y1-10) <= row['Nose_y'] <= (CageLeftCorner_y2+10)) or ((CageLeftCorner_x1-10) <= int(row['Centroid_x']) <= (CageLeftCorner_x2+10)) and ((CageLeftCorner_y1-10) <= row['Centroid_y'] <= (CageLeftCorner_y2+10))):
            Cage_time = round((Cage_time + (1/fps)), 2)
            cageFrameNoList.append(index)
        if index >= secondsToAnalyze:
            break
    outPutDataFilePath = os.path.join(outPutDataPath, currentTrackingFramedFolder + '.csv')
    videoName_List.append(currentTrackingFramedFolder)
    topCornerList.append(topLeftCorner_time)
    BottomLeftCornerList.append(BottomLeftCorner_time)
    cageTime_List.append(Cage_time)
    indDf.Time_top_corner.iloc[topLeftFrameNoList] = 1
    indDf.Time_bottom_corner.iloc[bottomLeftFrameNoList] = 1
    indDf.Time_bottom_corner.iloc[bottomLeftFrameNoList] = 1
    indDf.Time_cage.iloc[cageFrameNoList] = 1
    indDf.to_csv(outPutDataFilePath)
    print(currentTrackingFile + ' done')
outputDf['Video'] = videoName_List
outputDf['Time top left corner'] = topCornerList
outputDf['Time bottom right corner'] = BottomLeftCornerList
outputDf[['Time top left corner', 'Time bottom right corner']] = outputDf[['Time top left corner', 'Time bottom right corner']].apply(pd.to_numeric)
outputDf['Total corner time'] = outputDf['Time top left corner'] + outputDf['Time bottom right corner']
outputDf['Cage time'] = cageTime_List


present_videos = outputDf[outputDf['Video'].str.contains("PRESENT")]
absent_videos = outputDf[outputDf['Video'].str.contains("ABSENT")]
present_videos.columns = ['Video_present', 'Time_top_left_corner_present', 'Time_bottom_right_corner_present', 'Total_corner_time_present', 'Cage_time_present']
absent_videos.columns = ['Video_absent', 'Time_top_left_corner_absent', 'Time_bottom_right_corner_absent', 'Total_corner_time_absent', 'Cage_time_absent']

CD1_present_videos = present_videos[present_videos['Video_present'].str.contains("_CD1_")]
CD1_present_videos = CD1_present_videos.reset_index()
Familar_present_videos = present_videos[present_videos['Video_present'].str.contains("_FAMILIAR_")]
Familar_present_videos = Familar_present_videos.reset_index()
Nonfamiliar_present_videos = present_videos[present_videos['Video_present'].str.contains("_NONFAMILIAR_")]
Nonfamiliar_present_videos = Nonfamiliar_present_videos.reset_index()
CD1_absent_videos = absent_videos[absent_videos['Video_absent'].str.contains("CD1")]
CD1_absent_videos = CD1_absent_videos.reset_index()
Familar_absent_videos = absent_videos[absent_videos['Video_absent'].str.contains("_FAMILIAR_")]
Familar_absent_videos = Familar_absent_videos.reset_index()
Nonfamiliar_absent_videos = absent_videos[absent_videos['Video_absent'].str.contains("_NONFAMILIAR_")]
Nonfamiliar_absent_videos = Nonfamiliar_absent_videos.reset_index()

CD1_df = pd.concat([CD1_absent_videos, CD1_present_videos], axis=1)
CD1_df = CD1_df.reset_index()
Familiar_df = pd.concat([Familar_absent_videos,Familar_present_videos ], axis=1)
Familiar_df = Familiar_df.reset_index()
Nonfamiliar_df = pd.concat([Nonfamiliar_absent_videos, Nonfamiliar_present_videos], axis=1)
Nonfamiliar_df = Nonfamiliar_df.reset_index()

printDf = pd.concat([CD1_df, Familiar_df, Nonfamiliar_df], ignore_index=True)
printDf['Social interaction ratio'] = printDf['Cage_time_present'] / printDf['Cage_time_absent']
printDf['Status'] = np.where(printDf['Social interaction ratio'] > 0.999999999999999999, 'R', 'S')
printDf = printDf.drop(['index_0', 'index', 'level_0'], axis=1)
summaryFilePath = os.path.join(outPutDataPath, 'Summary.csv')
printDf.to_csv(summaryFilePath, index=False)
