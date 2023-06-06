# Import library
import os
import pandas as pd
import json

# Create dataframe
data = {'Question': [], 'Answer': [], 'Correct': [], 'Title': []}
data_json = []
df = pd.DataFrame(data)

# Passing all txt file in folder
list_file_txt = os.listdir('txt_folder')
for ele in list_file_txt:
    # Open txt file
    with open(os.path.join('txt_folder',ele),'r',encoding="utf-8") as file:
        txt_file = file.read()
    
    # Split each question-answer base on @@@
    list_QA = txt_file.split('@@@')

    # Passing all question-answer
    for ele in list_QA:
        info = ele.split('|||')
        title, question, answer, correct = info[0], info[1].replace('^^^','\n'), info[2].replace('^^^','\n'), info[3]
        
        # Update to csv file
        df.loc[len(df)] = [question,answer,correct,title]

        # Update to json file
        temp_dict = {}
        temp_dict.update({'Question':question})
        temp_dict.update({'Answer':answer.split('^^^')})
        temp_dict.update({'Correct':correct.split('^^^')})
        temp_dict.update({'Title':title})
        data_json.append(temp_dict)


file_name = str(input('Input subject name: '))
# Save info to csv file
df.to_csv(os.path.join('csv_folder',f'{file_name}.csv'),index=False)

# Save info to json file
json_file_path = os.path.join('json_folder',f'{file_name}.json')
with open(json_file_path, 'w') as json_file:
    json.dump(data_json, json_file, indent=4)

print('Merge Complete!!!')
