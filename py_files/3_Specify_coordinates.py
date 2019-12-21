import os
import cv2
import pandas as pd
import numpy as np
import time
videoFilesFound = []
videoDir = r"Z:\DeepLabCut\OpenField_analysis\videos"

coordDf = pd.DataFrame(columns=['Top_left_corner_top_left_x', 'Top_left_corner_top_left_y', 'Top_left_corner_bottom_right_x', 'Top_left_corner_bottom_right_y', \
                                'Bottom_left_corner_top_left_x', 'Bottom_left_corner_top_left_y', 'Bottom_left_corner_bottom_right_x', 'Bottom_left_corner_bottom_right_y',  \
                                'Cage_top_left_x', 'Cage_left_corner_top_left_y', 'Cage_left_corner_bottom_right_x', 'Cage_left_corner_bottom_right_y'])
coordDfList = []
topLeft = True
bottomRight = False
rectangleComplete = False


# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy
    global cordStatus
    global topLeft, bottomRight, rectangleComplete
    if (event == cv2.EVENT_LBUTTONDBLCLK):
        print(x,y)
        cv2.circle(overlay,(x,y),16,(144,0,255),-1)
        cordList.append(x)
        cordList.append(y)
        topLeft = False
        bottomRight = True
        if len(cordList) == 4:
            rectangleComplete = True
            bottomRight = False

for i in os.listdir(videoDir):
    if i.__contains__(".mp4"):
        file = os.path.join(videoDir, i)
        videoFilesFound.append(file)

for i in videoFilesFound:
    currentVideo = i
    currentVideoName = os.path.basename(currentVideo)
    currentDir = str(os.path.dirname(currentVideo))
    cap = cv2.VideoCapture(currentVideo)
    cap.set(1, 0)
    ret, frame = cap.read()
    fileName = str(0) + str('.bmp')
    filePath = os.path.join(currentDir, fileName)
    cv2.imwrite(filePath, frame)
    img = cv2.imread(filePath)
    origImage = img.copy()
    overlay = img.copy()
    ix, iy = -1, -1
    cordList = []
    cv2.namedWindow('Select coordinates: double left mouse click at two locations. Press ESC when done', cv2.WINDOW_NORMAL)

    while(1):
        if (rectangleComplete == False):
            if (topLeft == True):
                cv2.setMouseCallback('Select coordinates: double left mouse click at two locations. Press ESC when done',draw_circle)
                cv2.putText(overlay, 'Double left click at the top left corner of the box', (200, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                cv2.putText(overlay, 'Video: ' + str(currentVideoName), (200, 150), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Select coordinates: double left mouse click at two locations. Press ESC when done', overlay)
                overlay = origImage.copy()
                k = cv2.waitKey(20) & 0xFF
                if k == 27:
                    break
            if (bottomRight == True):
                cv2.circle(overlay, (cordList[0], cordList[1]), 16, (144, 0, 255), -1)
                cv2.putText(overlay, 'Double left click at the bottom right corner of the box', (400, 900), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255), 2)
                cv2.putText(overlay, 'Video: ' + str(currentVideoName), (400, 950), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 255))
                cv2.imshow('Select coordinates: double left mouse click at two locations. Press ESC when done', overlay)
                cv2.setMouseCallback('Select coordinates: double left mouse click at two locations. Press ESC when done', draw_circle)
                k = cv2.waitKey(20) & 0xFF
                if k == 27:
                    break
        if (rectangleComplete == True):
            overlay = origImage.copy()
            cv2.rectangle(overlay, (cordList[0], cordList[1]), (cordList[2], cordList[3]), (0, 0, 255), 2)
            k = cv2.waitKey(20) & 0xFF
            bottomLeftCorner = [cordList[0], cordList[3]]
            topRightCorner = [cordList[2], cordList[1]]
            topLeftCorner = [cordList[0], cordList[1]]
            bottomRightCorner = [cordList[2], cordList[3]]
            pxDistanceBottomLeft2TopLeft = (np.sqrt((bottomLeftCorner[0] - topRightCorner[0]) ** 2 + (bottomLeftCorner[1] - topRightCorner[1]) ** 2))
            rearCornerSize = int(pxDistanceBottomLeft2TopLeft * 0.20)
            bottomLeftSquareBottomRightCorner = [bottomLeftCorner[0]+rearCornerSize, bottomLeftCorner[1]]
            bottomLeftSquareTopLeftCorner = [bottomLeftCorner[0], bottomLeftCorner[1]-rearCornerSize]
            topLeftSquareTopLeftCorner = [topLeftCorner[0], topLeftCorner[1]]
            topLeftSquareBottomRightCorner = [topLeftCorner[0]+rearCornerSize, topLeftCorner[1]+rearCornerSize]
            bottomRightCornerCage = [bottomRightCorner[0], bottomRightCorner[1] - rearCornerSize]
            topLeftCornerCage = [bottomRightCornerCage[0] - rearCornerSize, topRightCorner[1] + rearCornerSize]
            cv2.rectangle(overlay, (bottomLeftSquareTopLeftCorner[0], bottomLeftSquareTopLeftCorner[1]), (bottomLeftSquareBottomRightCorner[0], bottomLeftSquareBottomRightCorner[1]), (0, 0, 255), 2)
            cv2.rectangle(overlay, (topLeftSquareTopLeftCorner[0], topLeftSquareTopLeftCorner[1]), (topLeftSquareBottomRightCorner[0], topLeftSquareBottomRightCorner[1]), (0, 0, 255), 2)
            cv2.rectangle(overlay, (topLeftCornerCage[0], topLeftCornerCage[1]), (bottomRightCornerCage[0], bottomRightCornerCage[1]), (0, 0, 255), 2)
            cv2.putText(overlay, 'Press ESC to continue', (500, 600), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 3)
            cv2.imshow('Select coordinates: double left mouse click at two locations. Press ESC when done', overlay)
            k = cv2.waitKey(0) & 0xFF
            if k == 27:
                break
    coordDf.loc[currentVideoName] = [topLeftSquareTopLeftCorner[0], topLeftSquareTopLeftCorner[1], topLeftSquareBottomRightCorner[0], topLeftSquareBottomRightCorner[1], bottomLeftSquareTopLeftCorner[0], bottomLeftSquareTopLeftCorner[1], bottomLeftSquareBottomRightCorner[0],bottomLeftSquareBottomRightCorner[1], topLeftCornerCage[0], topLeftCornerCage[1], bottomRightCornerCage[0], bottomRightCornerCage[1]]
    topLeft = True
    bottomRight = False
    rectangleComplete = False
coordDf.to_csv('coordinates.csv')
