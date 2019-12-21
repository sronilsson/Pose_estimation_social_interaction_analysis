import os
import pandas as pd
import math
import numpy as np
import statistics

trackingFilesList = []
trackingFilesDir = r"Z:\DeepLabCut\OpenField_analysis\tracking_data"
criterion = 2
loopy = 0


def add_correction_prefix(col, bpcorrected_list):
    colc = 'Corrected_' + col
    bpcorrected_list.append(colc)
    return bpcorrected_list

def correct_value_position(df, colx, coly, col_corr_x, col_corr_y, dict_pos):

    dict_pos[colx] = dict_pos.get(colx, 0) 
    dict_pos[coly] = dict_pos.get(coly, 0)

    animalSize = mean1size

    currentCriterion = mean1size * criterion
    list_x = []
    list_y = []
    prev_x = df.iloc[0][colx]
    prev_y = df.iloc[0][coly]
    ntimes = 0
    live_prevx = df.iloc[0][colx]
    live_prevy = df.iloc[0][coly]
    NT = 12
    for index, row in df.iterrows():

        if index == 0:
            continue

        if (math.hypot(row[colx] - prev_x, row[coly] - prev_y) < (animalSize/4)): #the mouse is standing still
            currentCriterion = animalSize * 2
            
        if ((math.hypot(row[colx] - prev_x, row[coly] - prev_y) < currentCriterion) or (ntimes > NT and \
                                      math.hypot(row[colx] - live_prevx, row[coly] - live_prevy) < currentCriterion)):

            list_x.append(row[colx])
            list_y.append(row[coly])

            prev_x = row[colx]
            prev_y = row[coly]

            ntimes = 0
            
        else:
            #out of range
            list_x.append(prev_x)
            list_y.append(prev_y)
            dict_pos[colx] += 1
            dict_pos[coly] += 1
            ntimes += 1
            
        live_prevx = row[colx]
        live_prevy = row[coly]
        
    df[col_corr_x] = list_x
    df[col_corr_y] = list_y

    return df

########### FIND CSV FILES ###########
for i in os.listdir(trackingFilesDir):
    if i.__contains__(".csv"):
        file = os.path.join(trackingFilesDir, i)
        trackingFilesList.append(file)

########### CREATE PD FOR RAW DATA AND PD FOR MOVEMENT BETWEEN FRAMES ###########
for i in trackingFilesList:
    loopy += 1
    currentFile = i
    csv_df = pd.read_csv(currentFile,
                            names=["Nose_x", "Nose_y","Nose_p","Left_ear_x", "Left_ear_y", "Left_ear_p", "Right_ear_x", "Right_ear_y", "Right_ear_p", "Centroid_x", "Centroid_y", "Centroid_p", "Tail_base_x", "Tail_base_y", "Tail_base_p"])
    csv_df = csv_df.drop(csv_df.index[[0, 1, 2]])
    csv_df = csv_df.apply(pd.to_numeric)
    ########### CREATE SHIFTED DATAFRAME FOR DISTANCE CALCULATIONS ###########################################
    csv_df_shifted = csv_df.shift(periods=1)
    csv_df_shifted = csv_df_shifted.rename(columns={'Nose_x': 'Nose_x_shifted', 'Nose_y': 'Nose_y_shifted', 'Nose_p': 'Nose_p_shifted', 'Left_ear_x': 'Left_ear_x_shifted', \
                                        'Left_ear_y': 'Left_ear_y_shifted', 'Left_ear_p': 'Left_ear_p_shifted', 'Right_ear_x': 'Right_ear_x_shifted', 'Right_ear_y': 'Right_ear_y_shifted', \
                                        'Right_ear_p': 'Right_ear_p_shifted', 'Centroid_x': 'Centroid_x_shifted', 'Centroid_y': 'Centroid_y_shifted', 'Centroid_p': 'Centroid_p_shifted', 'Tail_base_x': \
                                        'Tail_base_x_shifted', 'Tail_base_y': 'Tail_base_y_shifted', 'Tail_base_p': 'Tail_base_p_shifted'})
    csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner')

    ########### EUCLIDEAN DISTANCES ###########################################
    csv_df_combined['Mouse_1_nose_to_tail'] = np.sqrt((csv_df_combined.Nose_x - csv_df_combined.Tail_base_x) ** 2 + (csv_df_combined.Nose_y - csv_df_combined.Tail_base_y) ** 2)
    csv_df_combined['Movement_mouse_1_centroid'] = np.sqrt((csv_df_combined.Centroid_x_shifted - csv_df_combined.Centroid_x) ** 2 + (csv_df_combined.Centroid_y_shifted - csv_df_combined.Centroid_y) ** 2)
    csv_df_combined['Movement_mouse_1_nose'] = np.sqrt((csv_df_combined.Nose_x_shifted - csv_df_combined.Nose_x) ** 2 + (csv_df_combined.Nose_y_shifted - csv_df_combined.Nose_y) ** 2)
    csv_df_combined['Movement_mouse_1_tail_base'] = np.sqrt((csv_df_combined.Tail_base_x_shifted - csv_df_combined.Tail_base_x) ** 2 + (csv_df_combined.Tail_base_y_shifted - csv_df_combined.Tail_base_y) ** 2)
    csv_df_combined['Movement_mouse_1_left_ear'] = np.sqrt((csv_df_combined.Left_ear_x_shifted - csv_df_combined.Left_ear_x) ** 2 + (csv_df_combined.Left_ear_x - csv_df_combined.Left_ear_y) ** 2)
    csv_df_combined['Movement_mouse_1_right_ear'] = np.sqrt((csv_df_combined.Right_ear_x_shifted - csv_df_combined.Right_ear_x) ** 2 + (csv_df_combined.Right_ear_x - csv_df_combined.Right_ear_y) ** 2)
    csv_df_combined = csv_df_combined.fillna(0)

    ########### MEAN MOUSE SIZES ###########################################
    mean1size = (statistics.mean(csv_df_combined['Mouse_1_nose_to_tail']))

    bps = ['Nose', 'Left_ear', 'Right_ear', 'Centroid', 'Tail_base']
    bplist1x = []
    bplist1y = []
    bpcorrected_list1x = []
    bpcorrected_list1y = []

    for bp in bps:
        colx = bp + '_x'
        coly = bp + '_y'
        bplist1x.append(colx)
        bplist1y.append(coly)
        bpcorrected_list1x = add_correction_prefix(colx, bpcorrected_list1x)
        bpcorrected_list1y = add_correction_prefix(coly, bpcorrected_list1y)

    # this dictionary will count the number of times each body part position needs to be corrected
    dict_pos = {}
    
    for idx, col1x in enumerate(bplist1x):
        # apply function to all body part data
        col1y = bplist1y[idx]
        col_corr_1x = bpcorrected_list1x[idx]
        col_corr_1y = bpcorrected_list1y[idx]
        csv_df_combined = correct_value_position(csv_df_combined, col1x, col1y, col_corr_1x, col_corr_1y, dict_pos)

    scorer = pd.read_csv(currentFile).scorer.iloc[2:]
    scorer = pd.to_numeric(scorer)
    scorer = scorer.reset_index()
    scorer = scorer.drop(['index'], axis=1)
    csv_df_combined['scorer'] = scorer.values.astype(int)
    csv_df_combined = csv_df_combined[
        ["scorer", "Corrected_Nose_x", "Corrected_Nose_y", "Nose_p", "Corrected_Left_ear_x", "Corrected_Left_ear_y", "Left_ear_p", "Corrected_Right_ear_x",
         "Corrected_Right_ear_y", "Right_ear_p", "Corrected_Centroid_x", "Corrected_Centroid_y", "Centroid_p", "Corrected_Tail_base_x", "Corrected_Tail_base_y", "Tail_base_p"]]
         
    #csv_df_combined = csv_df_combined.drop(csv_df_combined.index[0:2])
    df_headers = pd.read_csv(currentFile, nrows=0)
    csv_df_combined.columns = df_headers.columns
    csv_df_combined = pd.concat([df_headers, csv_df_combined])
    fileName = os.path.basename(currentFile)
    fileName, fileEnding = fileName.split('.')
    fileOut = str(fileName) + str('.csv')
    pathOut = os.path.join(trackingFilesDir, fileOut)
    csv_df_combined.to_csv(pathOut, index=False)
