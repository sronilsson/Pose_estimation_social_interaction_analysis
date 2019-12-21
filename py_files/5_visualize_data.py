import os
import cv2
import pandas as pd
from collections import deque

trackingFilesList = []
listPaths_mouse1 = deque(maxlen=600)
trackingFilesDir = r"Z:\DeepLabCut\OpenField_analysis\tracking_data"
inputFramesDir = r"Z:\DeepLabCut\OpenField_analysis\input_frames"
outputFramesDir = r"Z:\DeepLabCut\OpenField_analysis\output_frames"

coordinateFilePath = r"Z:\DeepLabCut\OpenField_analysis\py_files\coordinates.csv"
coordinateFileDf = pd.read_csv(coordinateFilePath)
fps = 30
secondsToAnalyze = 150 * fps


for i in os.listdir(trackingFilesDir):
    if i.__contains__(".csv"):
        file = os.path.join(trackingFilesDir, i)
        trackingFilesList.append(file)

for i in trackingFilesList:
    loop = 0
    topLeftCorner_time = 0
    BottomLeftCorner_time = 0
    Cage_time = 0
    CurrTrackFileDf = pd.read_csv(i,  names=["scorer","Nose_x", "Nose_y","Nose_p","Left_ear_x", "Left_ear_y", "Left_ear_p", "Right_ear_x", "Right_ear_y", "Right_ear_p", "Centroid_x", "Centroid_y", "Centroid_p", "Tail_base_x", "Tail_base_y", "Tail_base_p"])
    CurrTrackFileDf = CurrTrackFileDf.drop(CurrTrackFileDf.index[[0]])
    CurrTrackFileDf.drop(['scorer'], axis=1)
    CurrTrackFileDf = CurrTrackFileDf.apply(pd.to_numeric)
    CurrTrackFileDf = CurrTrackFileDf.astype(int)
    trackingFilename = os.path.basename(i).replace('.csv', '')
    videoFileName = str(trackingFilename) + '.mp4'
    CurrInputFramesDir = os.path.join(inputFramesDir, trackingFilename)
    CurrOutputFramesDir = os.path.join(outputFramesDir, trackingFilename)
    if not os.path.exists(CurrOutputFramesDir):
        os.makedirs(CurrOutputFramesDir)
    videoSettings = coordinateFileDf.loc[coordinateFileDf['Unnamed: 0'] == videoFileName]
    print(videoSettings)
    topLeft_x1 = int(videoSettings['Top_left_corner_top_left_x'])
    topLeft_x2 = int(videoSettings['Top_left_corner_bottom_right_x'])
    topLeft_y1 = int(videoSettings['Top_left_corner_top_left_y'])
    topLeft_y2 = int(videoSettings['Top_left_corner_bottom_right_y'])
    BottomLeft_x1 = int(videoSettings['Bottom_left_corner_top_left_x'])
    BottomLeft_x2 = int(videoSettings['Bottom_left_corner_bottom_right_x'])
    BottomLeft_y1 = int(videoSettings['Bottom_left_corner_top_left_y'])
    BottomLeft_y2 = int(videoSettings['Bottom_left_corner_bottom_right_y'])
    CageLeft_x1 = int(videoSettings['Cage_top_left_x'])
    CageLeft_x2 = int(videoSettings['Cage_left_corner_bottom_right_x'])
    CageLeft_y1 = int(videoSettings['Cage_left_corner_top_left_y'])
    CageLeft_y2 = int(videoSettings['Cage_left_corner_bottom_right_y'])

    for index, row in CurrTrackFileDf.iterrows():
        imageName = str(loop) + '.png'
        imageNameSave = str(loop) + '.bmp'
        inputImgPath = os.path.join(CurrInputFramesDir, imageName)
        im = cv2.imread(inputImgPath)
        cv2.rectangle(im, (topLeft_x1, topLeft_y1), (topLeft_x2, topLeft_y2), (255, 0, 0), 2)
        cv2.rectangle(im, (BottomLeft_x1, BottomLeft_y1), (BottomLeft_x2, BottomLeft_y2), (255, 191, 0), 2)
        cv2.rectangle(im, (CageLeft_x1, CageLeft_y1), (CageLeft_x2, CageLeft_y2), (255, 255, 0), 2)
        cv2.circle(im, (row['Left_ear_x'], row['Left_ear_y']), 8, (255, 20, 147), thickness=-1, lineType=8, shift=0)
        cv2.circle(im, (row['Right_ear_x'], row['Right_ear_y']), 8, (139, 0, 139), thickness=-1, lineType=8,shift=0)
        cv2.circle(im, (row['Nose_x'], row['Nose_y']), 8, (210, 105, 30), thickness=-1, lineType=8,shift=0)
        cv2.circle(im, (row['Centroid_x'], row['Centroid_y']), 8, (64, 224, 208), thickness=-1, lineType=8,shift=0)
        cv2.circle(im, (row['Tail_base_x'], row['Tail_base_y']), 8, (255, 105, 180), thickness=-1, lineType=8,shift=0)
        if (((topLeft_x1-10) <= int(row['Nose_x']) <= (topLeft_x2+10)) and ((topLeft_y1-10) <= row['Nose_y'] <= (topLeft_y2+10)) or ((topLeft_x1-10) <= int(row['Centroid_x']) <= (topLeft_x2+10)) and ((topLeft_y1-10) <= row['Centroid_y'] <= (topLeft_y2+10))):
            topLeftCorner_time = round((topLeftCorner_time + (1 / fps)), 2)
        if (((BottomLeft_x1-10) <= int(row['Nose_x']) <= (BottomLeft_x2+10)) and ((BottomLeft_y1-10) <= row['Nose_y'] <= (BottomLeft_y2+10)) or ((BottomLeft_x1-10) <= int(row['Centroid_x']) <= (BottomLeft_x2+10)) and ((BottomLeft_y1-10) <= row['Centroid_y'] <= (BottomLeft_y2+10))):
            BottomLeftCorner_time = round((BottomLeftCorner_time + (1 / fps)), 2)
        if (((CageLeft_x1-10) <= int(row['Nose_x']) <= (CageLeft_x2+10)) and ((CageLeft_y1-10) <= row['Nose_y'] <= (CageLeft_y2+10)) or ((CageLeft_x1-10) <= int(row['Centroid_x']) <= (CageLeft_x2+10)) and ((CageLeft_y1-10) <= row['Centroid_y'] <= (CageLeft_y2+10))):
            Cage_time = round((Cage_time + (1 / fps)), 2)
        cv2.putText(im, ('Top left time: ' + str(topLeftCorner_time) + 's'), (750, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(im, ('Bottom left time: ' + str(BottomLeftCorner_time) + 's'), (750, 650), cv2.FONT_HERSHEY_SIMPLEX, 1, (64, 224, 208), 2)
        cv2.putText(im, ('Cage time: ' + str(Cage_time) + 's'), (750, 700), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        imageSavePath = os.path.join(CurrOutputFramesDir, imageNameSave)
        print(imageSavePath)
        cv2.imwrite(imageSavePath, im)
        loop+=1













