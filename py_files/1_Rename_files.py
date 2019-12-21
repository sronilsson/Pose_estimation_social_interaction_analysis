import os
import cv2
import pandas as pd
trackingFilesList = []

trackingFilesDir = r"Z:\DeepLabCut\OpenField_analysis\tracking_data"

for i in os.listdir(trackingFilesDir):
    if i.__contains__(".csv"):
        file = os.path.join(trackingFilesDir, i)
        trackingFilesList.append(file)

for old_file_name_path in trackingFilesList:
    old_file_name = os.path.basename(old_file_name_path)
    newName, toDelete = old_file_name.split('Deep')
    newName = newName + '.csv'
    new_file_name_path = os.path.join(trackingFilesDir, newName)

    os.rename(old_file_name_path, new_file_name_path)


