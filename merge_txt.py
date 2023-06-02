# Import library
import os
import pandas as pd
import json
from datetime import datetime

# Create dataframe
data = {'Question': [], 'Answer': [], 'Correct': [], 'Title': []}
data_json = []
df = pd.DataFrame(data)

# Passing all txt file in folder
list_file_txt = os.listdir('txt_folder')
for ele in list_file_txt:
    # Open txt file
    with open(os.path.join('txt_folder',ele),'r') as file:
        txt_file = file.read()
    
    # Split each question-answer base on @@@
    list_QA = txt_file.split('@@@')

    # Passing all question-answer
    for ele in list_QA:
        info = ele.split('|||')
        title, question, answer, correct = info[0], info[1], info[2], info[3]
        
        # Update to csv file
        df.loc[len(df)] = [question,answer,correct,title]

        # Update to json file
        temp_dict = {}
        temp_dict.update({'Question':question})
        temp_dict.update({'Answer':answer})
        temp_dict.update({'Correct':correct})
        temp_dict.update({'Title':title})
        data_json.append(temp_dict)


current_time = datetime.now()
formatted_time = current_time.strftime("%d-%m-%Y-%Hh-%Mp-%Ss")
# Save info to csv file
df.to_csv(os.path.join('csv_folder',f'{formatted_time}.csv'),index=False)

# Save info to json file
json_file_path = os.path.join('json_folder',f'{formatted_time}.json')
with open(json_file_path, 'w') as json_file:
    json.dump(data_json, json_file, indent=4)

print('Merge Complete!!!')


        