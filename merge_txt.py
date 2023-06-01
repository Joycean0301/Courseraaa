# Import library
import os
import pandas as pd

# Create dataframe
data = {'Question': [], 'Answer': [], 'Correct': [], 'Title': []}
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
        df.loc[len(df)] = [question,answer,correct,title]

# Save info to csv file
df.to_csv('file.csv',index=False)

print('Merge Complete!!!')


        